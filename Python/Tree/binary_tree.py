from collections import deque

class binary_tree_node:
    def __init__(self, val: int):
        self.val: int = val
        self.left_tree: binary_tree_node | None = None
        self.right_tree: binary_tree_node | None = None

# 层序遍历：BFS
def level_order(tree: binary_tree_node | None):
    if tree is None:
        return

    queue = deque([tree])
    while queue:
        node = queue.popleft()
        print(node.val)

        if node.left_tree:
            queue.append(node.left_tree)
        if node.right_tree:
            queue.append(node.right_tree)

# 前序遍历：根 → 左 → 右
def pre_order(tree: binary_tree_node | None):
    if tree is None:
        return

    print(tree.val)
    pre_order(tree.left_tree)
    pre_order(tree.right_tree)

# 中序遍历：左 → 根 → 右
def mid_order(tree: binary_tree_node | None):
    if tree is None:
        return

    mid_order(tree.left_tree)
    print(tree.val)
    mid_order(tree.right_tree)

# 后序遍历：左 → 右 → 根
def last_order(tree: binary_tree_node | None):
    if tree is None:
        return

    last_order(tree.left_tree)
    last_order(tree.right_tree)
    print(tree.val)