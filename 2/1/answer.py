import typing


def count_letters(line: str) -> typing.Tuple[bool, bool]:
    letter_count = {}
    for letter in line:
        letter_count[letter] = letter_count.get(letter, 0) + 1

    two = False
    three = False
    for count in letter_count.values():
        if count == 2:
            two = True
        elif count == 3:
            three = True
        if two and three:
            return two, three

    return two, three


def main():
    with open('inputs\\input02.txt', 'r') as file_input:
        two_count = 0
        three_count = 0
        for line in file_input:
            two, three = count_letters(line)
            if two:
                two_count += 1
            if three:
                three_count += 1

    answer = two_count * three_count
    print(f'{two_count} * {three_count} = {answer}')


if __name__ == '__main__':
    main()
