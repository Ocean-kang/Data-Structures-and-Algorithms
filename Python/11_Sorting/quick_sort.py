def partition(nums: list[int], left: int, right: int):
    base = nums[left]
    # 划分
    while left < right:
        # 右边
        while left < right and nums[right] >= base:
            right -= 1
        nums[left] = nums[right]
        if left < right:          # 相遇就不再跳
            left += 1

        # 左边
        while left < right and nums[left] <= base:
            left += 1
        nums[right] = nums[left]
        if left < right:          # 相遇就不再跳
            right -= 1
    # 放 base
    nums[left] = base
    return left

def partition_official(nums: list[int], left: int, right: int) -> int:
    """哨兵划分"""
    # 以 nums[left] 为基准数
    i, j = left, right
    while i < j:
        while i < j and nums[j] >= nums[left]:
            j -= 1  # 从右向左找首个小于基准数的元素
        while i < j and nums[i] <= nums[left]:
            i += 1  # 从左向右找首个大于基准数的元素
        # 元素交换
        nums[i], nums[j] = nums[j], nums[i]
    # 将基准数交换至两子数组的分界线
    nums[i], nums[left] = nums[left], nums[i]
    return i  # 返回基准数的索引

def quick_sort(nums: list[int], left: int, right: int):
    if left >= right:
        return nums

    # 完整
    base = partition(nums, left, right)
    quick_sort(nums, left, base - 1)
    quick_sort(nums, base + 1, right)
    return nums