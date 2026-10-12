"""
链表的学习使用
"""

class Node:
    def init(self, val: int):
        self.val: int = val
        self.next: Node | None = None

class ListNode:
    """链表节点类"""
    def __init__(self, val: int):
        self.val: int = val               # 节点值
        self.next: ListNode | None = None # 指向下一节点的引用

def ListNodes_init():
    # 初始化链表 1 -> 3 -> 2 -> 5 -> 4
    # 初始化各个节点
    n0 = ListNode(1)
    n1 = ListNode(3)
    n2 = ListNode(2)
    n3 = ListNode(5)
    n4 = ListNode(4)
    # 构建节点之间的引用
    n0.next = n1
    n1.next = n2
    n2.next = n3
    n3.next = n4
    return n0

def print_listnode(listnode: ListNode) -> None:
    head = listnode
    while head != None:
        print(head.val)
        head = head.next
    return None

def insert_linkedlist(head: ListNode, val: int) -> ListNode:
    listnode_val = ListNode(val=val)
    listnode_val.next = head.next
    head.next = listnode_val
    return head

def insert(n0: ListNode, P: ListNode):
    """在链表的节点 n0 之后插入节点 P"""
    n1 = n0.next
    P.next = n1
    n0.next = P
    return None

def remove(n0: ListNode):
    """删除链表的节点 n0 之后的首个节点"""
    if not n0.next:
        return
    # n0 -> P -> n1
    P = n0.next
    n1 = P.next
    n0.next = n1

def access(head: ListNode | None, index: int) -> ListNode | None:
    """访问链表中索引为 index 的节点"""
    for _ in range(index):
        if not head:
            return None
        head = head.next
    return head

def find(head: ListNode | None, target: int) -> int:
    """在链表中查找值为 target 的首个节点"""
    index = 0
    while head:
        if head.val == target:
            return index
        head = head.next
        index += 1
    return -1

if __name__ == "__main__":

    n0 = ListNode(1)
    n1 = ListNode(2)
    n2 = ListNode(3)

    # 构建节点之间的引用
    n0.next = n1
    n1.next = n2
    # 打印
    print_listnode(n0)
    # 应用
    # ---------------------------
    access(n0, 1)

    # ---------------------------
    # 打印
    print_listnode(n0)