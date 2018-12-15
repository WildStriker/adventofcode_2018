import re


def get_new_value(section, patterns):
    for pattern_state, replace in patterns:
        if pattern_state == section:
            return replace
    return '.'


def main():
    with open('inputs\\input12.txt') as file_input:
        match = re.search(r'[#\.]+', file_input.readline())
        state = '.....' + match.group(0) + '.....'
        min_pot = -5

        # skip line
        file_input.readline()

        patterns = []
        pattern = re.compile(r'([#\.]{5}) => ([#\.])\n*')
        for line in file_input:
            match = pattern.match(line)
            pattern_state = match.group(1)
            replace = match.group(2)
            patterns.append((pattern_state, replace))

        print(f'0: {state}')
        new_state = state
        for generation in range(1, 21):
            if state[:5] != '.....':
                state = '.....' + state
                new_state = state
                min_pot -= 5
            if state[-5:] != '.....':
                state = state + '.....'
                new_state = state

            for current_pot in range(2, len(state)):
                section = state[current_pot-2:current_pot+3]
                new_value = get_new_value(section, patterns)
                new_state = new_state[:current_pot] + \
                    new_value + new_state[current_pot+1:]
            state = new_state
            print(f'{generation}: {new_state}')
            pot_sum = 0
        for current_pot, current_state in enumerate(state):
            if current_state == '#':
                pot_sum += min_pot + current_pot
        print(f'post sum:{pot_sum}')


if __name__ == "__main__":
    main()
