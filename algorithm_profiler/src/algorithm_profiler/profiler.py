"""Single-threaded, synchronous algorithm measurements using the standard library."""

from __future__ import annotations

import inspect
import sys
import threading
import time
import tracemalloc
from functools import wraps
from types import CodeType, FrameType
from typing import Any, Callable, ParamSpec, TypeVar, overload

P = ParamSpec("P")
R = TypeVar("R")
_state = threading.local()


class _CallDepth:
    """Count active Python calls below the target, excluding profiler frames."""

    def __init__(self, target_code: CodeType) -> None:
        self.target_code = target_code
        self.root_frame: FrameType | None = None
        self.depth = 0
        self.maximum = 0
        self.finished = False

    def __call__(self, frame: FrameType, event: str, arg: Any) -> None:
        if self.finished or event not in ("call", "return"):
            return

        if self.root_frame is None:
            if event == "call" and frame.f_code is self.target_code:
                self.root_frame = frame
                self.depth = 1
                self.maximum = 1
            return

        # Recursive decorated calls pass through wrapper(); it is not an
        # algorithm frame. Helpers defined by the caller still count normally.
        if frame.f_globals is globals():
            return

        if event == "call":
            self.depth += 1
            self.maximum = max(self.maximum, self.depth)
        else:
            self.depth -= 1
            if frame is self.root_frame:
                self.root_frame = None
                self.finished = True


def _print_report(
    name: str,
    elapsed_ns: int,
    peak_bytes: int | None,
    depth: int | None,
    time_complexity: str | None,
    space_complexity: str | None,
    exception_name: str | None,
) -> None:
    memory_text = (
        f"{peak_bytes / 1024:.2f} KiB"
        if peak_bytes is not None
        else "N/A (tracemalloc is already active)"
    )
    depth_text = (
        str(depth)
        if depth is not None
        else "N/A (a profile hook is already active)"
    )
    lines = [
        f"Function: {name}",
        f"Elapsed time: {elapsed_ns / 1_000_000:.6f} ms",
        f"Peak Python memory increase: {memory_text}",
        f"Max Python call depth: {depth_text}",
        f"Theoretical time complexity: {time_complexity or 'Not specified'}",
        f"Theoretical space complexity: {space_complexity or 'Not specified'}",
    ]
    if exception_name is not None:
        lines.append(f"Exception: {exception_name}")
    print("\n".join(lines))


def _run_profiled(
    function: Callable[P, R],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    time_complexity: str | None,
    space_complexity: str | None,
) -> R:
    # Bound methods keep their Python code on __func__.
    target = function.__func__ if inspect.ismethod(function) else function
    counter = _CallDepth(target.__code__)
    previous_profile = sys.getprofile()
    memory_already_active = tracemalloc.is_tracing()
    owns_profile = False
    owns_memory = False
    baseline = 0
    peak_bytes: int | None = None
    started_ns: int | None = None
    elapsed_ns = 0
    exception_name: str | None = None

    try:
        if not memory_already_active:
            tracemalloc.start()
            owns_memory = True
            baseline, _ = tracemalloc.get_traced_memory()
            tracemalloc.reset_peak()

        if previous_profile is None:
            sys.setprofile(counter)
            owns_profile = True

        started_ns = time.perf_counter_ns()
        try:
            return function(*args, **kwargs)
        except BaseException as exc:
            exception_name = type(exc).__name__
            raise
        finally:
            elapsed_ns = time.perf_counter_ns() - started_ns
    finally:
        # Restore instrumentation even when the algorithm raises. A failed
        # setup must also release any instrumentation already acquired.
        try:
            if owns_profile:
                sys.setprofile(previous_profile)
        finally:
            counter.root_frame = None
            if owns_memory:
                try:
                    _, peak = tracemalloc.get_traced_memory()
                    peak_bytes = max(0, peak - baseline)
                finally:
                    tracemalloc.stop()

        if started_ns is not None:
            try:
                _print_report(
                    function.__qualname__,
                    elapsed_ns,
                    peak_bytes,
                    counter.maximum if owns_profile else None,
                    time_complexity,
                    space_complexity,
                    exception_name,
                )
            except Exception:
                # A broken output stream must not replace an algorithm's
                # original exception. On success, output failures still surface.
                if exception_name is None:
                    raise


@overload
def profile_algorithm(
    function: Callable[P, R],
    *,
    time_complexity: str | None = None,
    space_complexity: str | None = None,
) -> Callable[P, R]: ...


@overload
def profile_algorithm(
    function: None = None,
    *,
    time_complexity: str | None = None,
    space_complexity: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def profile_algorithm(
    function: Callable[P, R] | None = None,
    *,
    time_complexity: str | None = None,
    space_complexity: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """Print measurements and optional Big O labels; return the original result.

    Use as ``@profile_algorithm`` or ``@profile_algorithm(...)``. Only the
    outermost decorated call prints a report. Python call depth starts at one
    for the target function and includes Python helpers but not this module.

    This measures synchronous, single-threaded algorithms. Time includes the
    instrumentation cost, and memory is a traced Python allocation peak rather
    than total process memory or an exact byte count of the call stack.
    """

    def decorate(target: Callable[P, R]) -> Callable[P, R]:
        if not (inspect.isfunction(target) or inspect.ismethod(target)):
            raise TypeError(
                "profile_algorithm supports synchronous Python functions "
                "and methods only."
            )
        # unwrap() also catches generator/async functions hidden by a
        # cooperative decorator that uses functools.wraps().
        unwrapped = inspect.unwrap(target)
        for candidate in (target, unwrapped):
            if (
                inspect.iscoroutinefunction(candidate)
                or inspect.isgeneratorfunction(candidate)
                or inspect.isasyncgenfunction(candidate)
            ):
                raise TypeError(
                    "profile_algorithm does not support async functions "
                    "or generators. Use a synchronous function instead."
                )

        @wraps(target)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if getattr(_state, "active", False):
                return target(*args, **kwargs)

            _state.active = True
            try:
                return _run_profiled(
                    target, args, kwargs, time_complexity, space_complexity
                )
            finally:
                _state.active = False

        return wrapper

    if function is None:
        return decorate
    return decorate(function)
