from collections import deque

class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int):
        self.val: int = val                # 节点值
        self.left: TreeNode | None = None  # 左子节点引用
        self.right: TreeNode | None = None # 右子节点引用

def level_order(root: TreeNode | None) -> list[int]:
    """层序遍历"""
    if root is None:
        return []
    # 初始化队列，加入根节点
    queue: deque[TreeNode] = deque()
    queue.append(root)
    # 初始化一个列表，用于保存遍历序列
    res = []
    while queue:
        node: TreeNode = queue.popleft()  # 队列出队
        res.append(node.val)  # 保存节点值
        if node.left is not None:
            queue.append(node.left)  # 左子节点入队
        if node.right is not None:
            queue.append(node.right)  # 右子节点入队
    return res

def pre_order(root: TreeNode | None) -> list[int]:
    res = []

    def dfs(node):
        if node is None:
            return

        res.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return res

def in_order(root: TreeNode | None) -> list[int]:
    res = []

    def dfs(node):
        if node is None:
            return

        dfs(node.left)
        res.append(node.val)
        dfs(node.right)

    dfs(root)
    return res

def post_order(root: TreeNode | None) -> list[int]:
    res = []

    def dfs(node):
        if node is None:
            return

        dfs(node.left)
        dfs(node.right)
        res.append(node.val)

    dfs(root)
    return res