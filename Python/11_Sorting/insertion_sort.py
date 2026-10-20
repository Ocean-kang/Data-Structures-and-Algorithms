def insert(nums, base_index):
    base = nums[base_index]
    j = base_index - 1
    while j >= 0 and nums[j] > base:
        nums[j+1] = nums[j]
        j -= 1
    nums[j+1] = base
    return nums

def insertion_sort(nums: list[int]) -> list[int]:
    """原地升序排序，并返回原列表。"""
    n = len(nums)
    for i in range(1, n):
        base_index = i
        insert(nums, base_index)
    return nums

def insertion_sort_official(nums: list[int]):
    """插入排序"""
    # 外循环：已排序区间为 [0, i-1]
    for i in range(1, len(nums)):
        base = nums[i]
        j = i - 1
        # 内循环：将 base 插入到已排序区间 [0, i-1] 中的正确位置
        while j >= 0 and nums[j] > base:
            nums[j + 1] = nums[j]  # 将 nums[j] 向右移动一位
            j -= 1
        nums[j + 1] = base  # 将 base 赋值到正确位置
    return nums
