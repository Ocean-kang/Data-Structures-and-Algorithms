class binary_tree_node:
    def __init__(self, val: int):
        self.val: int = val
        self.left_tree: binary_tree_node | None = None
        self.right_tree: binary_tree_node | None = None

# def level_order(tree: binary_tree_node):
#     print(tree.val)
#     if tree.left_tree:
#         level_order(tree.left_tree)
#     elif tree.right_tree:
#         level_order(tree.right_tree)
#     else:
#         return None

def pre_order(tree: binary_tree_node):
    print(tree.val)
    if tree.left_tree:
        pre_order(tree.left_tree)
    if tree.right_tree:
        pre_order(tree.right_tree)
    else:
        return None

def mid_order(tree: binary_tree_node):
    if tree.left_tree!=None or tree.left_tree!=None:
        if tree.left_tree:
            mid_order(tree.left_tree)
            print(tree.val)
        if tree.right_tree:
            mid_order(tree.right_tree)
    else:
        print(tree.val)
    return None

def last_order(tree: binary_tree_node):
    if tree.left_tree!=None or tree.left_tree!=None:
        if tree.left_tree:
            last_order(tree.left_tree)
        if tree.right_tree:
            last_order(tree.right_tree)
            print(tree.val)
    else:
        print(tree.val)
    return None