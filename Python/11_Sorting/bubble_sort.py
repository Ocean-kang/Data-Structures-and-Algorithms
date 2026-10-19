
def bubble_sort(nums: list[int]):
    n = len(nums)
    for i in range(n, 0, -1):
        exchange: bool = False
        for j in range(i-1):
            if nums[j] <= nums[j+1]:
                continue
            else:
                nums[j], nums[j+1] = nums[j+1], nums[j]
                exchange = True
        if not exchange:
            break
    return nums

def bubble_sort_official(nums: list[int]):
    """冒泡排序"""
    n = len(nums)
    # 外循环：未排序区间为 [0, i]
    for i in range(n - 1, 0, -1):
        # 内循环：将未排序区间 [0, i] 中的最大元素交换至该区间的最右端
        for j in range(i):
            if nums[j] > nums[j + 1]:
                # 交换 nums[j] 与 nums[j + 1]
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums