import typing


class Node:
    def __init__(self, children: typing.List['Node'], entries: list):
        self._children = children
        self._entries = entries

    def sum_entries(self):
        return sum(self._entries)

    def sum_children_by_entries(self):
        if not self._children:
            return sum(self._entries)

        total = 0
        for entry in self._entries:
            if entry <= len(self._children):
                total += self._children[entry - 1].sum_children_by_entries()

        return total


def get_node(numbers: typing.List[str], index) -> Node:
    child_count = int(numbers[index])
    index += 1
    entries_count = int(numbers[index])

    # get children
    children = []
    for _ in range(child_count):
        index += 1
        index, node = get_node(numbers, index)
        children.append(node)

    # get entries
    entries = []
    for _ in range(entries_count):
        index += 1
        entries.append(int(numbers[index]))

    node = Node(children, entries)

    return index, node


def get_root(numbers: typing.List[str]):
    _, root_node = get_node(numbers, 0)
    return root_node


def main():
    with open('inputs\\input08.txt') as file_input:
        numbers = file_input.read().split(' ')
        root_node: Node = get_root(numbers)
        print(root_node.sum_children_by_entries())


if __name__ == "__main__":
    main()
