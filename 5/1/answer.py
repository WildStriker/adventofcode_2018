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
        polymer = input_file.read()

    output = react_polymer(polymer)

    print(len(output))


if __name__ == "__main__":
    main()
