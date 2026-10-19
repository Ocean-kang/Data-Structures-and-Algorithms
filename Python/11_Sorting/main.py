# from selection_sort import selection_sort as sorting
# from bubble_sort import bubble_sort as sorting
from insertion_sort import insertion_sort as sorting

if __name__ == "__main__":
    nums_1 = [1,2,3,4,5,6,7]
    nums_2 = [1,3,5,7,9,8,6]
    nums_3 = [9,8,7,6,5,4,3,2,1]
    nums_4 = [5,4,4,3,2,2,1,1]

    label1 = "Official Python sorted() Result"
    label2 = "My Sorting() Result"
    w = max(len(label1), len(label2))

    print(f"{label1:<{w}} = {sorted(nums_1)}")
    print(f"{label2:<{w}} = {sorting(nums_1)}")
    print(f"{label1:<{w}} = {sorted(nums_2)}")
    print(f"{label2:<{w}} = {sorting(nums_2)}")
    print(f"{label1:<{w}} = {sorted(nums_3)}")
    print(f"{label2:<{w}} = {sorting(nums_3)}")
    print(f"{label1:<{w}} = {sorted(nums_4)}")
    print(f"{label2:<{w}} = {sorting(nums_4)}")