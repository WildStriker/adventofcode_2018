import re


def plot_clay(input_file):
    clays = set()
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    for line in input_file:
        match = re.match('([xy])=([0-9]+), ([yx])=([0-9]+)..([0-9]+)', line)
        coord_1 = match.group(1)
        range_1 = [int(match.group(2))]

        range_2 = range(int(match.group(4)), int(match.group(5))+1)

        if coord_1 == 'x':
            x_range = range_1
            y_range = range_2
        else:
            x_range = range_2
            y_range = range_1

        for y_coord in y_range:
            if not min_y or y_coord < min_y:
                min_y = y_coord
            if not max_y or y_coord > max_y:
                max_y = y_coord
            for x_coord in x_range:

                if not min_x or x_coord < min_x:
                    min_x = x_coord
                if not max_x or x_coord > max_x:
                    max_x = x_coord

                coords = (y_coord, x_coord)
                clays.add(coords)
    return clays, min_y, max_y, min_x, max_x


def main():
    with open('inputs\\input17.txt') as input_file:
        clays, min_y, max_y, min_x, max_x = plot_clay(input_file)

    water = (0, 500)
    first_drip = (1, 500)
    complete_path = set([first_drip])
    drip_ends = set([first_drip])
    filled = set()

    while drip_ends:
        new_row = []
        # go down
        drip_end: tuple = drip_ends.pop()

        new_coords = (drip_end[0] + 1, drip_end[1])
        while new_coords[0] <= max_y and not new_coords in clays and not new_coords in filled:
            complete_path.add(new_coords)
            drip_end = new_coords
            new_coords = (new_coords[0] + 1, new_coords[1])

        if drip_end[0] < max_y:
            new_row.append(drip_end)

            # go left
            fill = True
            new_coords = (drip_end[0], drip_end[1]-1)
            coord_below = (new_coords[0] + 1, new_coords[1])
            while not new_coords in clays and not new_coords in filled:
                new_row.append(new_coords)
                if not coord_below in clays and not coord_below in filled:
                    fill = False
                    drip_ends.add(new_coords)
                    break
                new_coords = (new_coords[0], new_coords[1]-1)
                coord_below = (new_coords[0] + 1, new_coords[1])

            # go right
            new_coords = (drip_end[0], drip_end[1]+1)
            coord_below = (new_coords[0] + 1, new_coords[1])
            while not new_coords in clays and not new_coords in filled:
                new_row.append(new_coords)
                if not coord_below in clays and not coord_below in filled:
                    fill = False
                    drip_ends.add(new_coords)
                    break
                new_coords = (new_coords[0], new_coords[1]+1)
                coord_below = (new_coords[0] + 1, new_coords[1])

            # fill
            complete_path.update(set(new_row))
            if fill:
                while new_row:
                    filled.add(new_row.pop())
                drip_end = (drip_end[0] - 1, drip_end[1])
                drip_ends.add(drip_end)

    for y_pos in range(min_y, max_y + 15):
        line = []
        for x_pos in range(min_x - 1, max_x + 15):
            coords = (y_pos, x_pos)
            if coords == water:
                line.append('+')
            elif coords in clays:
                line.append('#')
            elif coords in filled:
                line.append('~')
            elif coords in complete_path:
                line.append('|')
            else:
                line.append('.')
        print(' '.join(line))

    print(f'Whole path: {len(complete_path)}')
    filtered = list(filter(lambda coords: coords[0] >= min_y, complete_path))
    print(f'Filtered range: {len(filtered)}')
    print(f'Filled Tiles:{len(filled)}')


if __name__ == "__main__":
    main()
