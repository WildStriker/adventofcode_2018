def convert_string(number: str) -> int:
    if number[0] == '+':
        return int(number[1:])
    else:
        return int(number)


def main():
    with open('inputs\\input01.txt') as file_input:
        numbers_sum = sum(map(convert_string, file_input))

    print(numbers_sum)


if __name__ == '__main__':
    main()
