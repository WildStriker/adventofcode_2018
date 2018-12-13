def react_polymer(polymer):
    output = []
    last_letter: str = None
    for letter in polymer:
        if last_letter and last_letter != letter and last_letter.lower() == letter.lower():
            output_last = len(output) - 1
            del output[output_last]
            if output:
                last_letter = output[output_last - 1]
            else:
                last_letter = None
        else:
            output.append(letter)
            last_letter = letter
    return output


def main():
    with open('inputs\\input05.txt') as input_file:
        polymer: str = input_file.read()

    start_code = ord('A')
    end_code = ord('Z') + 1

    shortest = None
    for letter_code in range(start_code, end_code):
        letter = chr(letter_code)
        remove_unit = polymer.replace(letter, '')
        remove_unit = remove_unit.replace(letter.lower(), '')
        output_count = len(react_polymer(remove_unit))
        if not shortest or output_count < shortest:
            shortest = output_count

    print(shortest)


if __name__ == "__main__":
    main()
