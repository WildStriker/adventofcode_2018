import typing


def scan_for_letters(id_1: str, id_2: str) -> str:
    same_letters = ''
    different_count = 0
    for index, letter_id_1 in enumerate(id_1):
        letter_id_2 = id_2[index]
        if letter_id_1 == letter_id_2:
            same_letters += letter_id_1
        else:
            different_count += 1
            if different_count > 1:
                return None

    return same_letters


def get_same_letters(lines: typing.List[str]) -> str:
    for index_1, id_1 in enumerate(lines):
        for index_2, id_2 in enumerate(lines):
            if index_1 != index_2:
                box_id = scan_for_letters(id_1, id_2)
                if box_id:
                    return box_id

    return None


def main():
    with open('inputs\\input02.txt') as file_input:
        lines = file_input.read().splitlines()

    box_id = get_same_letters(lines)
    print(box_id)


if __name__ == "__main__":
    main()
