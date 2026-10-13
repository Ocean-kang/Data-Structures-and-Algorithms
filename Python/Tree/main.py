from binary_tree import *
from binary_tree_official import *

if __name__ == '__main__':
    # 初始化二叉树
    # 初始化节点
    n1 = TreeNode(val=1)
    n2 = TreeNode(val=2)
    n3 = TreeNode(val=3)
    n4 = TreeNode(val=4)
    n5 = TreeNode(val=5)
    # 构建节点之间的引用（指针）
    n1.left = n2
    n1.right = n3
    n2.left = n4
    n2.right = n5

    # 初始化二叉树
    # 初始化节点
    n1 = binary_tree_node(val=1)
    n2 = binary_tree_node(val=2)
    n3 = binary_tree_node(val=3)
    n4 = binary_tree_node(val=4)
    n5 = binary_tree_node(val=5)
    # 构建节点之间的引用（指针）
    n1.left_tree = n2
    n1.right_tree = n3
    n2.left_tree = n4
    n2.right_tree = n5

    pre_order(n1)
    mid_order(n1)
    last_order(n1)