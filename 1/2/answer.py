import typing


def next_frequency(numbers: typing.List[int]) -> int:
    frequency = 0
    while True:
        for number in numbers:
            frequency += number
            yield frequency


def convert_string(number: str) -> int:
    if number[0] == '+':
        return int(number[1:])
    else:
        return int(number)


def get_repeat_frequency(numbers: typing.List[int]) -> int:
    known_frequency = set()
    for number in next_frequency(numbers):
        if number in known_frequency:
            return number
        known_frequency.add(number)


def main():
    with open('inputs\\input01.txt') as file_input:
        numbers = list(map(convert_string, file_input))

    repeat_frequency = get_repeat_frequency(numbers)
    print(repeat_frequency)


if __name__ == '__main__':
    main()
