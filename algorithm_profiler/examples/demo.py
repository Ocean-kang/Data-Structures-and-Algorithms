"""Run after installing the package: python algorithm_profiler/examples/demo.py."""

from algorithm_profiler import profile_algorithm


@profile_algorithm(time_complexity="O(n)", space_complexity="O(1)")
def linear_search(items: list[int], target: int) -> int:
    """顺序查找：最坏情况下遍历整个数组。"""
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


@profile_algorithm(time_complexity="O(n)", space_complexity="O(n)")
def recursive_sum(items: list[int], index: int = 0) -> int:
    """递归求和：使用索引，避免切片造成额外复制。"""
    if index == len(items):
        return 0
    return items[index] + recursive_sum(items, index + 1)


if __name__ == "__main__":
    values = [3, 1, 4, 1, 5]

    print("--- Iterative search ---")
    found = linear_search(values, 5)
    print(f"Returned index: {found}\n")

    print("--- Recursive sum ---")
    total = recursive_sum(values)
    print(f"Returned sum: {total}")
