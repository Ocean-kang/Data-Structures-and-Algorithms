# Algorithm Profiler

给数据结构与算法练习使用的 Python 装饰器。函数仍返回原结果，每次最外层调用结束后，在终端打印英文性能报告。运行时仅使用 Python 标准库，支持 Python 3.10 及以上。

## 安装与运行

在仓库根目录使用运行学习脚本的同一个 Python 环境执行：

```shell
python -m pip install -e ./algorithm_profiler
python algorithm_profiler/examples/demo.py
```

安装后，仓库中任何学习脚本都可以直接导入，无需手动修改 `sys.path`。这个目录也是独立项目，可以复制到其他地方后安装。

## 使用

```python
from algorithm_profiler import profile_algorithm


@profile_algorithm(time_complexity="O(n)", space_complexity="O(1)")
def find(items, target):
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


result = find([1, 3, 5], 5)
assert result == 2
```

输出示例（耗时和内存数值仅作示意）：

```text
Function: find
Elapsed time: 0.123456 ms
Peak Python memory increase: 1.25 KiB
Max Python call depth: 1
Theoretical time complexity: O(n)
Theoretical space complexity: O(1)
```

也可以使用 `@profile_algorithm` 或 `@profile_algorithm()`，不传复杂度参数；理论复杂度显示为 `Not specified`。复杂度参数是你根据算法填写的说明，装饰器不会检查或自动推断它。示例中的查找时间复杂度表示最坏情况，输入规模 `n` 是数组长度。

支持实例方法，装饰器不会改变参数、返回对象、函数名称或文档字符串。与 `@classmethod` 或 `@staticmethod` 一起使用时，把 `@profile_algorithm` 放在靠近 `def` 的位置。

## 如何理解这些指标

| 英文字段 | 含义 |
| --- | --- |
| `Elapsed time` | 单次调用的实际经过时间，包含等待、函数自身打印，以及测量工具在执行期间的开销；不包含报告打印。单位为毫秒。 |
| `Peak Python memory increase` | 调用测量期间，Python 追踪内存相对起始基线的峰值增量。包含临时对象和本次创建的返回对象，也可能包含测量工具的少量分配开销。单位为 KiB（1024 字节）。 |
| `Max Python call depth` | 从目标函数开始，最多同时存在的 Python 函数调用层数。目标函数算第 1 层，辅助函数计入，装饰器内部帧和 C 函数调用不计入。 |
| `Theoretical time complexity` | 手动填写的理论时间复杂度。 |
| `Theoretical space complexity` | 手动填写的理论空间复杂度，建议注明是否采用辅助空间口径。 |

**一次运行的耗时、内存数值不等于 Big O。** 复杂度描述开销随输入规模的增长趋势，需要结合代码分析。相同复杂度的函数也可能有不同的实际耗时。

内存统计使用标准库 [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html)，只覆盖它能追踪的 Python 内存分配，不代表进程总内存、所有第三方原生内存或精确的栈帧字节数。调用前已存在的输入对象本身不计入本次新增分配，但调用期间创建的输出对象计入；这个指标不等同于理论辅助空间。

**栈深度也不等于空间字节数。** 递归通常会增加调用深度；每层创建的对象大小可能不同。Python 调用栈深度也不代表底层 C 栈的实际深度。

## 递归、嵌套和异常

- 递归和嵌套装饰函数只在最外层调用结束时打印一份报告，使用最外层函数填写的复杂度说明。
- `examples/demo.py` 对比迭代查找和递归求和。5 个元素的递归求和包含终止条件调用，最大深度为 6；迭代查找为 1。
- 被测函数只运行一次，不会为了测量而重复执行或复制输入，适合会修改数据结构的操作。
- 函数抛出异常时先打印报告，附加例如 `Exception: ValueError`，再重新抛出同一个异常。测量状态会被清理，后续调用可以正常测量。
- 调用前已有 `tracemalloc` 追踪时，内存字段显示 `N/A (tracemalloc is already active)`，保留原有追踪和峰值。
- 调用前已有 `sys.setprofile()` 钩子时，深度字段显示 `N/A (a profile hook is already active)`，保留原有钩子。

## 适用边界

第一版面向单线程同步算法。不支持多个线程同时测量，也不追踪算法创建的新线程。`tracemalloc` 的统计是进程级的，其他线程的分配可能混入测量结果；请在单线程练习脚本中使用。

异步函数、生成器函数和异步生成器会在装饰时抛出 `TypeError`，因为其实际工作不在普通函数调用返回前完成。请勿在被测函数内修改 `tracemalloc` 或 `sys.setprofile()` 状态。与其他装饰器叠加时，若同步包装器返回迭代器或协程对象，本工具不会继续驱动这些对象执行。

追踪内存和调用事件会影响实际耗时，特别是大量函数调用或深递归的代码。这里的数字适合学习观察，不能用作没有测量开销的精确基准。调用深度追踪也不会消除 Python 的递归深度限制。

## 测试

安装后在仓库根目录运行：

```shell
python -m unittest discover -s algorithm_profiler/tests -v
```
