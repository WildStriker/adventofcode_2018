import typing


class Instruction:
    def __init__(self, letter):
        self._letter = letter
        self._can_begin = {}
        self._conditions = {}
        self._is_completed = False

    @property
    def letter(self):
        return self._letter

    @property
    def conditions(self) -> typing.Dict[str, 'Instruction']:
        return self._conditions

    @property
    def can_begin(self) -> typing.Dict[str, 'Instruction']:
        return self._can_begin

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @is_completed.setter
    def is_completed(self, value: bool):
        self._is_completed = value

    def add_condition(self, condition: 'Instruction'):
        self._conditions[condition.letter] = condition

    def add_can_begin(self, can_begin: 'Instruction'):
        self._can_begin[can_begin.letter] = can_begin


def get_instructions(input_file) -> typing.Dict[str, Instruction]:
    instructions: typing.Dict[str, Instruction] = {}

    # list condition dict inside of
    for line in input_file:
        instruction = line[5]
        can_begin = line[36]

        instructions[can_begin] = instructions.get(
            can_begin, Instruction(can_begin))
        instructions[instruction] = instructions.get(
            instruction, Instruction(instruction))

        instructions[can_begin].add_condition(instructions[instruction])
        instructions[instruction].add_can_begin(instructions[can_begin])
    return instructions


def get_next_letters(instruction: Instruction, letter_order, next_letters: list = None):
    if not next_letters:
        next_letters = []

    for letter in instruction.can_begin.keys():
        if letter not in letter_order:
            next_letters.append(letter)
    return sorted(set(next_letters))


def get_order(instructions: typing.Dict[str, Instruction]) -> str:

    from_letter = ord('A')
    to_letter = ord('Z')

    letter_order = ''

    # find all with no conditions
    next_letters = []
    for letter_code in range(from_letter, to_letter + 1):
        letter = chr(letter_code)
        if letter in instructions:
            instruction = instructions[letter]
            if not instruction.conditions:
                next_letters.append(letter)

    next_letter = next_letters[0]
    # all known letters coming up
    next_letters = get_next_letters(instruction, letter_order, next_letters)

    while next_letters:
        # continue if all conditions met
        index = None
        for index, letter in enumerate(next_letters):
            is_next = True
            conditions: Instruction = instructions[letter].conditions
            for condition in conditions.values():
                condition: Instruction
                if not condition.is_completed:
                    is_next = False
                    break
            if is_next:
                break

        next_letter = next_letters.pop(index)
        instruction = instructions[next_letter]

        instruction.is_completed = True
        letter_order += next_letter
        next_letters = get_next_letters(
            instruction, letter_order, next_letters)

    return letter_order


def main():
    with open('inputs\\input07.txt') as input_file:
        # nested dictionary of steps and conditions
        instructions = get_instructions(input_file)

        order = get_order(instructions)
        print(order)


if __name__ == "__main__":
    main()
