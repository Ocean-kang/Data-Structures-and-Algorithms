'''Stack implemented using an array.'''
class ArraryStack:
    def __init__(self) -> None:
        self.stack = list()
        pass

    def push(self, val: int):
        self.stack.append(val)
        return None

    def pop(self):
        return self.stack.pop()

    def len_stack(self):
        return len(self.stack)

    def is_empty(self):
        return len(self.stack) == 0


'''Stack implemented using a linked list.'''
class LinkedListStack:
    def __init__(self, val: int) -> None:
        self.val = val
        pass