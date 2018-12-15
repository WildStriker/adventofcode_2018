import re


def get_new_value(current_pot, state, patterns):
    offset = -2
    for pattern_state, has_plant in patterns:
        matches_pattern = True
        for index, symbol in enumerate(pattern_state):
            index_state = current_pot + offset + index
            if symbol and not index_state in state or \
                    not symbol and index_state in state:
                matches_pattern = False
                break
        if matches_pattern:
            return has_plant
    return False


def main():
    with open('inputs\\input12.txt') as file_input:
        match = re.search(r'[#\.]+', file_input.readline())
        state = set()
        character_state = match.group(0)
        for count, character in enumerate(character_state):
            if character == '#':
                state.add(count)
        start_point = 0
        end_point = len(character_state) + 2

        # skip line
        file_input.readline()

        patterns = []
        pattern = re.compile(r'([#\.]{5}) => ([#\.])\n*')
        for line in file_input:
            match = pattern.match(line)
            pattern_state = []
            for symbol in match.group(1):
                if symbol == '#':
                    pattern_state.append(True)
                else:
                    pattern_state.append(False)
            has_plant = match.group(2) == '#'
            patterns.append((pattern_state, has_plant))

        previous_sum = 0
        repeat_diff_count = 0
        last_diff_sum = 0
        generation_count = None
        total_generation = 50000000000
        for generation_count in range(1, total_generation + 1):
            new_state = set()
            pot_sum = 0
            for current_pot in range(start_point, end_point + 1):
                has_plant = get_new_value(current_pot, state, patterns)
                if has_plant:
                    new_state.add(current_pot)
                    pot_sum += current_pot
                    if current_pot <= start_point + 1:
                        start_point -= 2
                    elif current_pot >= end_point - 1:
                        end_point += 2

            state = new_state
            new_diff = pot_sum - previous_sum
            if new_diff == last_diff_sum:
                repeat_diff_count += 1
            else:
                repeat_diff_count = 0

            last_diff_sum = new_diff
            previous_sum = pot_sum
            if repeat_diff_count == 10:
                break

        final_sum = pot_sum + last_diff_sum * \
            (total_generation - generation_count)
        print(final_sum)


if __name__ == "__main__":
    main()
