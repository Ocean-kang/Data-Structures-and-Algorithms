# from selection_sort import selection_sort as sorting
# from bubble_sort import bubble_sort as sorting
# from insertion_sort import insertion_sort as sorting
from quick_sort import quick_sort as sorting
# from merge_sort import merge_sort as sorting

if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 5, 7, 9, 8, 6],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [5, 4, 4, 3, 2, 2, 1, 1],
        [],
        [1],
        [2, 2, 2],
        [0, -2, 3, -1, 0],
    ]

    label1 = "Official Python sorted() Result"
    label2 = "My Sorting() Result"
    w = max(len(label1), len(label2))

    for case_number, nums in enumerate(test_cases, start=1):
        expected = sorted(nums)
        actual = sorting(nums.copy())

        print(f"{label1:<{w}} = {expected}")
        print(f"{label2:<{w}} = {actual}")
        assert actual == expected, (
            f"案例 {case_number} 排序失败：输入 {nums}，"
            f"预期 {expected}，实际 {actual}"
        )
