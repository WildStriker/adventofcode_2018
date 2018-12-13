import typing


class Node:
    def __init__(self, children: typing.List['Node'], entries: list):
        self._children = children
        self._entries = entries

    def sum_all_entries(self):
        total = 0
        for child in self._children:
            total += child.sum_all_entries()
        total += sum(self._entries)
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
        print(root_node.sum_all_entries())


if __name__ == "__main__":
    main()
