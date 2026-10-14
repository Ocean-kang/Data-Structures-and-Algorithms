import binary_tree as my
from binary_tree_official import *

if __name__ == '__main__':
    # 初始化二叉树
    # 初始化节点
    m1 = TreeNode(val=1)
    m2 = TreeNode(val=2)
    m3 = TreeNode(val=3)
    m4 = TreeNode(val=4)
    m5 = TreeNode(val=5)
    # 构建节点之间的引用（指针）
    m1.left = m2
    m1.right = m3
    m2.left = m4
    m2.right = m5

    # 初始化二叉树
    # 初始化节点
    n1 = my.binary_tree_node(val=1)
    n2 = my.binary_tree_node(val=2)
    n3 = my.binary_tree_node(val=3)
    n4 = my.binary_tree_node(val=4)
    n5 = my.binary_tree_node(val=5)
    # 构建节点之间的引用（指针）
    n1.left_tree = n2
    n1.right_tree = n3
    n2.left_tree = n4
    n2.right_tree = n5

    '''my algo'''
    my.pre_order(n1)
    my.mid_order(n1)
    my.last_order(n1)
    my.level_order(n1)

    '''official algo'''
    print(pre_order(m1))
    print(in_order(m1))
    print(post_order(m1))
    print(level_order(m1))