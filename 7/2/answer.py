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


def get_next_letters(instruction, instructions, letter_order, next_letters: set = None):
    if not next_letters:
        next_letters = set()

    for letter in instruction.can_begin.keys():
        if letter not in letter_order:
            next_letters.add(letter)
    next_letters = set(next_letters)

    # build sorted list of available letters
    available_for_worker = []
    for letter in next_letters:
        is_available = True
        conditions: Instruction = instructions[letter].conditions
        for condition in conditions.values():
            condition: Instruction
            if not condition.is_completed:
                is_available = False
                break
        if is_available:
            available_for_worker.append(letter)

    return sorted(available_for_worker, reverse=True), next_letters


def get_time(instructions: typing.Dict[str, Instruction], worker_count: int, base_time=60) -> str:

    from_letter = ord('A')
    to_letter = ord('Z')

    letter_order = ''

    workers = {}

    # find all with no conditions
    next_letters = set()
    for letter_code in range(from_letter, to_letter + 1):
        letter = chr(letter_code)
        if letter in instructions:
            instruction = instructions[letter]
            if not instruction.conditions:
                next_letters.add(letter)

    # all known letters coming up
    available_for_worker, next_letters = get_next_letters(
        instruction,
        instructions,
        letter_order,
        next_letters)

    total_time = 0
    while next_letters or not workers:
        # assign to workers
        if available_for_worker:
            while len(workers) < worker_count and available_for_worker:
                next_letter = available_for_worker.pop()
                next_letters.remove(next_letter)

                instruction = instructions[next_letter]

                worker = workers[instruction.letter] = {}
                worker['instruction'] = instruction
                worker['time'] = base_time + ord(next_letter) - from_letter + 1

        # do work
        if workers:
            worker_keys = list(workers.keys())
            did_work = False
            for worker_key in worker_keys:
                worker = workers[worker_key]
                if worker['time'] > 0:
                    worker['time'] -= 1
                    did_work = True
                if worker['time'] == 0:
                    instruction = worker['instruction']
                    instruction.is_completed = True
                    letter_order += instruction.letter
                    available_for_worker, next_letters = get_next_letters(
                        instruction,
                        instructions,
                        letter_order,
                        next_letters)
                    del workers[worker_key]
            if did_work:
                total_time += 1

    return letter_order, total_time


def main():
    with open('inputs\\input07.txt') as input_file:
        # nested dictionary of steps and conditions
        instructions = get_instructions(input_file)

        letters, time = get_time(instructions, 5)
        print(f'{letters} took {time} seconds to complete')


if __name__ == "__main__":
    main()
