"""
AVL Tree practice
"""

import typing
import collections


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 0


class Tree:
    def __init__(self):
        self.data = []
        self.free = []
        self.root = 0
        self.size = 0

    def get_len(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def get_node(self, index):
        return self.data[index]

    def get_root(self):
        return self.root

    @typing.overload
    def contains_helper(self, value) -> tuple[typing.Literal[False], list[int]]:
        ...

    @typing.overload
    def contains_helper(self, value) -> tuple[typing.Literal[True], list[int] | None]:
        ...

    def contains_helper(self, value) -> tuple[bool, list[int] | None]:
        current = self.root

        if value == self.data[current].value:
            return True, None

        visited = [self.root]

        while (
            self.data[current].left is not None or self.data[current].right is not None
        ):
            if value < self.data[current].value:
                current = self.data[current].left
            elif value > self.data[current].value:
                current = self.data[current].right

            if not current:
                return False, visited

            if value == self.data[current].value:
                return True, visited

            visited.append(current)

        return False, visited

    def contains(self, value):
        if self.is_empty():
            return None

        match self.contains_helper(value):
            case (False, _):
                return None
            case (True, None):
                return self.root
            case (True, indices):
                parent = indices[-1]

                if value < self.data[parent].value:
                    return self.data[parent].left
                elif value > self.data[parent].value:
                    return self.data[parent].right

    def insert_helper(self, value):
        if len(self.free) > 0:
            index = self.free.pop()
            self.data[index] = Node(value)
            return index
        else:
            self.data.append(Node(value))
            return self.get_len()

    def insert(self, value):
        if self.is_empty():
            self.size = 1
            self.data.append(Node(value))
            return 0

        found, visited = self.contains_helper(value)
        if found:
            return None

        parent = visited[-1]
        index = self.insert_helper(value)

        if value < self.data[parent].value:
            self.data[parent].left = index
        if value > self.data[parent].value:
            self.data[parent].right = index

        self.update_and_balance(visited)
        self.size += 1
        return index

    def rotate_left(self, index):
        left = self.data[index].left
        left_right = self.data[left].right

        self.data[index].left = left_right
        self.data[left].right = index

        self.update_height(index)
        self.update_height(left)

        return left

    def rotate_right(self, index):
        right = self.data[index].right
        right_left = self.data[right].left

        self.data[index].right = right_left
        self.data[right].left = index

        self.update_height(index)
        self.update_height(right)

        return right

    def rotate_left_right(self, index):
        left = self.data[index].left

        self.data[index].left = self.rotate_left(left)
        return self.rotate_right(index)

    def rotate_right_left(self, index):
        right = self.data[index].right

        self.data[index].right = self.rotate_right(right)
        return self.rotate_left(index)

    def update_height(self, index):
        node = self.data[index]
        left = node.left
        right = node.right

        left_height = -1
        right_height = -1

        if left is not None:
            left_height = self.data[left].height
        if right is not None:
            right_height = self.data[right].height

        self.data[index].height = 1 + max(left_height, right_height)

        return right_height - left_height

    def balance_node(self, index, balance_factor):
        node = self.data[index]

        match balance_factor:
            case -2:
                left = self.data[node.left]
                if left is not None:
                    return self.rotate_right(index)
                else:
                    return self.rotate_left_right(index)
            case 2:
                right = self.data[node.right]
                if right is not None:
                    return self.rotate_right(index)
                else:
                    return self.rotate_right_left(index)
            case _:
                return index

    def update_and_balance(self, visited):
        while len(visited) > 0:
            index = visited.pop()
            balance_factor = self.update_height(index)
            new_parent = self.balance_node(index, balance_factor)

            if len(visited) > 0:
                grandfather = self.data[visited[-1]]
                if index == grandfather.left:
                    self.data[visited[-1]].left = new_parent
                else:
                    self.data[visited[-1]].right = new_parent
            else:
                self.root = new_parent

    def clean_tail(self):
        popped = []
        while not self.data[-1]:
            self.data.pop()
            popped.append(len(self.data))
        self.free = [i for i in self.free if i in popped]

    def remove_root_helper(self, value):
        root = self.data[self.root]
        if value == root.value:
            return_val = None

            if self.size == 1:
                return_val = self.data.pop().value
                self.free.clear()
                self.data.clear()
                self.root = 0
                self.size = 0

            if not root.right:
                return_val = self.data[self.root].value
                self.free.append(self.root)
                self.root = root.left
                self.size -= 1
                self.clean_tail()

            if not root.left:
                return_val = self.data[self.root].value
                self.free.append(self.root)
                self.root = root.right
                self.size -= 1
                self.clean_tail()

            return True, return_val
        return False, None

    def remove(self, value):
        if self.is_empty():
            return None

        is_root, return_val = self.remove_root_helper(value)
        if return_val is not None:
            return return_val

        found, visited = self.contains_helper(value)
        if found and visited is None:
            visited = [self.root]
        elif not found:
            return None

        parent = visited[-1]
        parent_data = self.data[parent]

        index = self.root
        if not is_root:
            if value < parent_data.value:
                index = parent_data.left
            else:
                index = parent_data.right

        data = self.data[index]
        return_val = None

        if data.left is not None and data.right is not None:
            if not is_root:
                visited.append(index)

            left_data = self.data[data.left]
            right_data = self.data[data.right]

            current = None
            replace_index = None

            if left_data.height > right_data.height:
                current = data.left
                while left_data.right is not None:
                    visited.append(current)
                    current = left_data.right
                    left_data = self.data[current]

                if left_data.left is not None:
                    self.data[current], self.data[left_data.left] = (
                        self.data[left_data.left],
                        self.data[current],
                    )
                    replace_index = left_data.left
                else:
                    self.data[visited[-1]].right = None
                    replace_index = current
            else:
                current = data.right
                while right_data.left is not None:
                    visited.append(current)
                    current = right_data.left
                    right_data = self.data[current]

                if right_data.right is not None:
                    self.data[current], self.data[right_data.right] = (
                        self.data[right_data.right],
                        self.data[current],
                    )
                    replace_index = right_data.right
                else:
                    self.data[visited[-1]].left = None
                    replace_index = current

            self.free.append(replace_index)
            replace = Node(self.data[replace_index].value)
            self.data[replace_index] = None

            if data.left is not None:
                replace.left = data.left
            if data.right is not None:
                replace.right = data.right

            return_val = self.data[index].value
            self.data[index] = replace

        else:
            if not data.left and not data.right:
                if value < parent_data.value:
                    self.data[parent].left = None
                else:
                    self.data[parent].right = None
            elif data.left is not None:
                if value < parent_data.value:
                    self.data[parent].left = data.left
                else:
                    self.data[parent].right = data.left
            else:
                if value < parent_data.value:
                    self.data[parent].left = data.right
                else:
                    self.data[parent].right = data.right

            self.free.append(index)
            return_val = self.data[index].value
            self.data[index] = None

        self.update_and_balance(visited)
        self.clean_tail()
        self.size -= 1
        return return_val


class Iter:
    def __init__(self, data, root):
        self.data = data
        self.queue = collections.deque([root])

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.queue) > 0:
            current = self.data[self.queue.popleft()]

            if current.left is not None:
                self.queue.append(current.left)

            if current.right is not None:
                self.queue.append(current.right)

            return current.value
        else:
            raise StopIteration


if __name__ == "__main__":
    tree = Tree()

    for n in range(1000):
        tree.insert(n)

    for n in range(400, 600):
        tree.remove(n)

    iter_tree = Iter(tree.data, tree.get_root())
    for n in iter_tree:
        print(n)
