def merge(nums: list[int], left: int, mid: int, right: int):
    """合并左子数组和右子数组"""
    # 左子数组区间为 [left, mid], 右子数组区间为 [mid+1, right]
    # 创建一个临时数组 tmp ，用于存放合并后的结果
    tmp = [0] * (right - left + 1)
    # 初始化左子数组和右子数组的起始索引
    i, j, k = left, mid + 1, 0
    # 当左右子数组都还有元素时，进行比较并将较小的元素复制到临时数组中
    while i <= mid and j <= right:
        if nums[i] <= nums[j]:
            tmp[k] = nums[i]
            i += 1
        else:
            tmp[k] = nums[j]
            j += 1
        k += 1
    # 将左子数组和右子数组的剩余元素复制到临时数组中
    while i <= mid:
        tmp[k] = nums[i]
        i += 1
        k += 1
    while j <= right:
        tmp[k] = nums[j]
        j += 1
        k += 1
    # 将临时数组 tmp 中的元素复制回原数组 nums 的对应区间
    for k in range(0, len(tmp)):
        nums[left + k] = tmp[k]

def _merge_sort(nums: list[int], left: int, right: int) -> None:
    """归并排序"""
    # 终止条件
    if left >= right:
        return  # 当子数组长度不超过 1 时终止递归
    # 划分阶段
    mid = (left + right) // 2 # 计算中点
    _merge_sort(nums, left, mid)  # 递归左子数组
    _merge_sort(nums, mid + 1, right)  # 递归右子数组
    # 合并阶段
    merge(nums, left, mid, right)


def merge_sort(nums: list[int]) -> list[int]:
    """使用归并排序将列表原地升序排列，并返回原列表。"""
    _merge_sort(nums, 0, len(nums) - 1)
    return nums
