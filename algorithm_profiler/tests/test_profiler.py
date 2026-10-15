"""Behavior tests; exact runtime and allocator-dependent byte counts are avoided."""

import inspect
import io
import sys
import tracemalloc
import unittest
from contextlib import redirect_stdout
from functools import wraps
from unittest.mock import patch

from algorithm_profiler import profile_algorithm


class ProfileAlgorithmTests(unittest.TestCase):
    def setUp(self):
        # Depth/peak assertions require an otherwise uninstrumented process.
        # Do not disturb tracing installed by an external test runner.
        if sys.getprofile() is not None or tracemalloc.is_tracing():
            self.skipTest("Run these tests without external profiling or tracemalloc.")
        self.addCleanup(sys.setprofile, None)
        self.addCleanup(tracemalloc.stop)

    def capture(self, function, *args, **kwargs):
        output = io.StringIO()
        with redirect_stdout(output):
            result = function(*args, **kwargs)
        return result, output.getvalue()

    def peak_kib(self, report):
        line = next(
            line for line in report.splitlines()
            if line.startswith("Peak Python memory increase:")
        )
        return float(line.split(": ", 1)[1].split()[0])

    def test_return_identity_arguments_and_single_execution(self):
        result_object = []
        calls = []

        @profile_algorithm
        def operation(value, /, extra=2, *, enabled=True):
            calls.append((value, extra, enabled))
            return result_object

        result, report = self.capture(operation, 3, extra=4, enabled=False)
        self.assertIs(result, result_object)
        self.assertEqual(calls, [(3, 4, False)])
        self.assertEqual(report.count("Function:"), 1)
        self.assertIn("Max Python call depth: 1\n", report)
        self.assertIn("Theoretical time complexity: Not specified", report)
        self.assertIn("Theoretical space complexity: Not specified", report)

    def test_no_arguments_factory_and_none_return(self):
        @profile_algorithm()
        def operation():
            return None

        result, report = self.capture(operation)
        self.assertIsNone(result)
        self.assertIn("Max Python call depth: 1\n", report)

    def test_manual_labels_are_printed_verbatim(self):
        @profile_algorithm(
            time_complexity="O(log n), worst case", space_complexity="O(1)"
        )
        def operation():
            return 42

        result, report = self.capture(operation)
        self.assertEqual(result, 42)
        self.assertIn("Theoretical time complexity: O(log n), worst case", report)
        self.assertIn("Theoretical space complexity: O(1)", report)

    def test_metadata_and_signature_are_preserved(self):
        def original(value: int, *, factor: int = 2) -> int:
            """An algorithm docstring."""
            return value * factor

        decorated = profile_algorithm(original)
        self.assertEqual(decorated.__name__, original.__name__)
        self.assertEqual(decorated.__qualname__, original.__qualname__)
        self.assertEqual(decorated.__doc__, original.__doc__)
        self.assertEqual(decorated.__annotations__, original.__annotations__)
        self.assertEqual(inspect.signature(decorated), inspect.signature(original))
        self.assertIs(decorated.__wrapped__, original)

    def test_instance_class_and_static_methods(self):
        class Stack:
            def __init__(self):
                self.items = []

            @profile_algorithm
            def push(self, item):
                self.items.append(item)
                return self.items

            @classmethod
            @profile_algorithm
            def kind(cls):
                return cls

            @staticmethod
            @profile_algorithm
            def empty():
                return []

        stack = Stack()
        result, report = self.capture(stack.push, 5)
        self.assertIs(result, stack.items)
        self.assertEqual(stack.items, [5])
        self.assertIn("Stack.push", report)
        self.assertIn("Max Python call depth: 1\n", report)
        self.assertIs(self.capture(Stack.kind)[0], Stack)
        self.assertEqual(self.capture(Stack.empty)[0], [])

    def test_an_already_bound_method_can_be_decorated(self):
        class Example:
            def get(self):
                return self

        instance = Example()
        result, report = self.capture(profile_algorithm(instance.get))
        self.assertIs(result, instance)
        self.assertIn("Max Python call depth: 1\n", report)

    def test_recursive_calls_produce_one_report_and_exclude_wrappers(self):
        @profile_algorithm(time_complexity="O(n)", space_complexity="O(n)")
        def recursive_sum(n):
            if n == 0:
                return 0
            return n + recursive_sum(n - 1)

        result, report = self.capture(recursive_sum, 5)
        self.assertEqual(result, 15)
        self.assertEqual(report.count("Function:"), 1)
        self.assertIn("Max Python call depth: 6\n", report)
        self.assertIn("Theoretical space complexity: O(n)", report)

    def test_python_helpers_count_and_c_calls_do_not(self):
        def leaf(items):
            return len(items)

        def middle(items):
            return leaf(items)

        @profile_algorithm
        def operation(items):
            return middle(items)

        result, report = self.capture(operation, [1, 2, 3])
        self.assertEqual(result, 3)
        self.assertIn("Max Python call depth: 3\n", report)

    def test_nested_decorators_use_outer_report_and_labels(self):
        @profile_algorithm(time_complexity="Inner label")
        def inner(value):
            return value + 1

        @profile_algorithm(time_complexity="Outer label")
        def outer(value):
            return inner(value)

        result, report = self.capture(outer, 4)
        self.assertEqual(result, 5)
        self.assertEqual(report.count("Function:"), 1)
        self.assertIn("outer", report)
        self.assertNotIn("Inner label", report)
        self.assertIn("Theoretical time complexity: Outer label", report)
        self.assertIn("Max Python call depth: 2\n", report)

        # The inner function is still independently measurable afterwards.
        self.assertIn("Max Python call depth: 1\n", self.capture(inner, 4)[1])

    def test_caught_helper_exception_balances_depth(self):
        def failing_helper():
            raise ValueError("handled")

        def helper():
            return 7

        @profile_algorithm
        def operation():
            try:
                failing_helper()
            except ValueError:
                return helper()

        result, report = self.capture(operation)
        self.assertEqual(result, 7)
        self.assertIn("Max Python call depth: 2\n", report)
        self.assertNotIn("Exception:", report)

    def test_exception_identity_report_and_cleanup(self):
        error = ValueError("original error")

        @profile_algorithm
        def fail():
            raise error

        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(ValueError) as caught:
            fail()
        self.assertIs(caught.exception, error)
        self.assertIn("Exception: ValueError", output.getvalue())
        self.assertIn("Max Python call depth: 1\n", output.getvalue())
        self.assertFalse(tracemalloc.is_tracing())
        self.assertIsNone(sys.getprofile())

        @profile_algorithm
        def succeed():
            return 9

        result, report = self.capture(succeed)
        self.assertEqual(result, 9)
        self.assertEqual(report.count("Function:"), 1)
        self.assertIn("Max Python call depth: 1\n", report)

    def test_base_exception_also_cleans_up(self):
        error = KeyboardInterrupt()

        @profile_algorithm
        def interrupt():
            raise error

        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(KeyboardInterrupt) as caught:
            interrupt()
        self.assertIs(caught.exception, error)
        self.assertIn("Exception: KeyboardInterrupt", output.getvalue())
        self.assertFalse(tracemalloc.is_tracing())
        self.assertIsNone(sys.getprofile())

    def test_temporary_allocation_is_captured_in_peak(self):
        @profile_algorithm
        def operation():
            temporary = bytearray(128 * 1024)
            length = len(temporary)
            del temporary
            return length

        result, report = self.capture(operation)
        self.assertEqual(result, 128 * 1024)
        self.assertGreaterEqual(self.peak_kib(report), 128)
        self.assertFalse(tracemalloc.is_tracing())
        self.assertIsNone(sys.getprofile())

    def test_new_return_objects_are_included_in_peak(self):
        @profile_algorithm
        def allocate():
            return bytearray(64 * 1024)

        result, report = self.capture(allocate)
        self.assertEqual(len(result), 64 * 1024)
        self.assertGreaterEqual(self.peak_kib(report), 64)

    def test_preexisting_input_is_not_counted_as_new_memory(self):
        existing = bytearray(1024 * 1024)

        @profile_algorithm
        def identity(value):
            return value

        result, report = self.capture(identity, existing)
        self.assertIs(result, existing)
        self.assertGreaterEqual(self.peak_kib(report), 0)
        self.assertLess(self.peak_kib(report), 1024)

    def test_elapsed_time_conversion(self):
        @profile_algorithm
        def operation():
            return 1

        with patch(
            "algorithm_profiler.profiler.time.perf_counter_ns",
            side_effect=[1_000_000, 2_250_000],
        ) as clock:
            result, report = self.capture(operation)
        self.assertEqual(result, 1)
        self.assertEqual(clock.call_count, 2)
        self.assertIn("Elapsed time: 1.250000 ms", report)

    def test_external_memory_tracing_and_peak_are_preserved(self):
        @profile_algorithm
        def operation():
            return 1

        tracemalloc.start()
        temporary = bytearray(512 * 1024)
        del temporary
        old_peak = tracemalloc.get_traced_memory()[1]
        result, report = self.capture(operation)
        self.assertEqual(result, 1)
        self.assertTrue(tracemalloc.is_tracing())
        self.assertGreaterEqual(tracemalloc.get_traced_memory()[1], old_peak)
        self.assertIn("N/A (tracemalloc is already active)", report)
        self.assertIn("Max Python call depth: 1\n", report)

    def test_external_profile_hook_keeps_receiving_events(self):
        events = []

        @profile_algorithm
        def operation():
            return 1

        def hook(frame, event, arg):
            if event == "call" and frame.f_code is operation.__wrapped__.__code__:
                events.append(event)

        sys.setprofile(hook)
        result, report = self.capture(operation)
        self.assertIs(sys.getprofile(), hook)
        self.assertEqual(result, 1)
        self.assertEqual(events, ["call"])
        self.assertIn("N/A (a profile hook is already active)", report)
        self.assertNotIn("N/A (tracemalloc is already active)", report)
        self.assertFalse(tracemalloc.is_tracing())

    def test_external_instrumentation_survives_algorithm_exception(self):
        def hook(frame, event, arg):
            pass

        @profile_algorithm
        def fail():
            raise RuntimeError("failed")

        sys.setprofile(hook)
        tracemalloc.start()
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(RuntimeError):
            fail()
        self.assertIs(sys.getprofile(), hook)
        self.assertTrue(tracemalloc.is_tracing())
        self.assertIn("N/A (tracemalloc is already active)", output.getvalue())
        self.assertIn("N/A (a profile hook is already active)", output.getvalue())
        self.assertIn("Exception: RuntimeError", output.getvalue())

    def test_failed_hook_setup_cleans_up_and_does_not_run_algorithm(self):
        calls = []

        @profile_algorithm
        def operation():
            calls.append(1)

        with patch(
            "algorithm_profiler.profiler.sys.setprofile",
            side_effect=RuntimeError("hook setup failed"),
        ):
            with self.assertRaisesRegex(RuntimeError, "hook setup failed"):
                self.capture(operation)
        self.assertEqual(calls, [])
        self.assertFalse(tracemalloc.is_tracing())
        self.assertIsNone(sys.getprofile())
        self.assertIn("Max Python call depth: 1\n", self.capture(operation)[1])

    def test_report_is_printed_after_measurement_cleanup(self):
        tracing_at_write = []

        class Output(io.StringIO):
            def write(self, text):
                tracing_at_write.append((tracemalloc.is_tracing(), sys.getprofile()))
                return super().write(text)

        @profile_algorithm
        def operation():
            return 1

        with redirect_stdout(Output()):
            operation()
        self.assertTrue(tracing_at_write)
        self.assertTrue(all(state == (False, None) for state in tracing_at_write))

    def test_report_failure_does_not_replace_algorithm_exception(self):
        error = ValueError("original error")

        @profile_algorithm
        def fail():
            raise error

        class BrokenOutput:
            def write(self, text):
                raise OSError("closed output")

        with redirect_stdout(BrokenOutput()), self.assertRaises(ValueError) as caught:
            fail()
        self.assertIs(caught.exception, error)
        self.assertFalse(tracemalloc.is_tracing())
        self.assertIsNone(sys.getprofile())

    def test_async_and_generators_rejected_at_decoration(self):
        async def coroutine():
            return 1

        def generator():
            yield 1

        async def async_generator():
            yield 1

        for function in (coroutine, generator, async_generator):
            for decorator in (profile_algorithm, profile_algorithm()):
                with self.subTest(function=function.__name__, decorator=decorator):
                    with self.assertRaisesRegex(TypeError, "async functions or generators"):
                        decorator(function)

    def test_wrapped_async_and_generators_are_also_rejected(self):
        def passthrough(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper

        async def coroutine():
            return 1

        def generator():
            yield 1

        for function in (coroutine, generator):
            with self.subTest(function=function.__name__):
                with self.assertRaises(TypeError):
                    profile_algorithm(passthrough(function))

    def test_non_python_function_rejected_clearly(self):
        for value in (len, 42, object()):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, "Python functions and methods only"):
                    profile_algorithm(value)


if __name__ == "__main__":
    unittest.main()
