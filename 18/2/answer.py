import collections
import copy


def load_acres(file_input):
    acres = []
    for line in file_input:
        row = []
        for acre in line.strip():
            row.append(acre)
        acres.append(row)
    return acres


def main():
    with open('inputs\\input18.txt') as file_input:
        acres = load_acres(file_input)

    area_y = len(acres)
    area_x = len(acres[0])

    open_acre = '.'
    tree_acre = '|'
    lumberyard_acre = '#'

    letter_count = collections.Counter()
    for row in acres:
        letter_count += collections.Counter(''.join(row))
    resource_value = letter_count[tree_acre] * \
        letter_count[lumberyard_acre]

    minutes = 1000000000
    y_coord = None
    x_coord = None

    resources = []
    resource_indexes = {}
    resource_counter = collections.Counter()
    start_index = None
    minute = None
    for minute in range(1, minutes + 1):
        new_state = copy.deepcopy(acres)
        for y_coord in range(area_y):
            adjacent_y_coords = list(range(
                max(y_coord - 1, 0), min(y_coord, area_y-2) + 2))

            for x_coord in range(area_x):
                current_acre = acres[y_coord][x_coord]

                adjacent_x_coords = list(range(
                    max(x_coord - 1, 0), min(x_coord, area_x-2) + 2))

                adjacent_acres = collections.Counter()
                for adjacent_y_coord in adjacent_y_coords:
                    for adjacent_x_coord in adjacent_x_coords:
                        if adjacent_y_coord != y_coord or adjacent_x_coord != x_coord:
                            adjacent_acre = acres[adjacent_y_coord][adjacent_x_coord]
                            adjacent_acres[adjacent_acre] += 1

                # open acre -> trees
                # if around at least three trees
                if current_acre == open_acre and \
                        tree_acre in adjacent_acres and adjacent_acres[tree_acre] >= 3:
                    new_state[y_coord][x_coord] = tree_acre

                # tree acre -> lumberyard
                # if around at least three lumberyards
                elif current_acre == tree_acre and \
                        lumberyard_acre in adjacent_acres and adjacent_acres[lumberyard_acre] >= 3:
                    new_state[y_coord][x_coord] = lumberyard_acre

                # lumberyard -> open
                # if not around lumberyard
                # or not around one tree.
                elif current_acre == lumberyard_acre and \
                        (lumberyard_acre not in adjacent_acres or tree_acre not in adjacent_acres):
                    new_state[y_coord][x_coord] = open_acre

        acres = new_state

        letter_count = collections.Counter()
        for row in new_state:
            letter_count += collections.Counter(''.join(row))

        resource_value = letter_count[tree_acre] * \
            letter_count[lumberyard_acre]

        state_string = ''
        for row in new_state:
            state_string += ''.join(row)

        resource_key = (letter_count[tree_acre],
                        letter_count[lumberyard_acre], resource_value, state_string)
        resources.append(resource_key)
        if resource_counter[resource_key] > 2:
            start_index = resource_indexes[resource_key]
            break
        else:
            resource_indexes[resource_key] = len(resources)
            resource_counter[resource_key] += 1

    pattern = resources[start_index:]

    minute_diff = minutes - minute - 1

    tree_count, \
        lumberyard_count, \
        resource_value, _ = pattern[minute_diff % len(pattern)]

    print(f'{tree_count} * {lumberyard_count} = {resource_value}')


if __name__ == "__main__":
    main()
