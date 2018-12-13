import itertools


def manhattan_distance(coords, x_coord, y_coord):
    return abs(coords[0] - x_coord) + abs(coords[1] - y_coord)

def get_closet_coords(coords_list, x_coord, y_coord):
    if (x_coord, y_coord) in coords_list:
        return [(x_coord, y_coord), ]

    min_distance = None
    min_distance_list = []

    for coords in coords_list:
        distance = manhattan_distance(coords, x_coord, y_coord)
        if not min_distance or distance < min_distance:
            min_distance = distance
            min_distance_list = [coords]
        elif distance == min_distance:
            min_distance_list.append(coords)
    return min_distance_list

def get_distance_total(coords_list, x_coord, y_coord, max_total=10000):
    total = 0
    for coords in coords_list:
        total += manhattan_distance(coords, x_coord, y_coord)
        if total >= max_total:
            return None
    return total


def main():
    with open('inputs\\input06.txt') as input_file:
        min_x = None
        max_x = None
        min_y = None
        max_y = None

        # get list of coords, keep track of min/max for infinities
        coords_list = set()
        for line in input_file:
            x_coord, y_coord = line.split(',')
            x_coord = int(x_coord)
            y_coord = int(y_coord)

            if not min_x or x_coord < min_x:
                min_x = x_coord
            if not max_x or x_coord > max_x:
                max_x = x_coord
            if not min_y or y_coord < min_y:
                min_y = y_coord
            if not max_y or y_coord > max_y:
                max_y = y_coord
            coords_list.add((x_coord, y_coord))

        # determine infinite coords, by scaning outside of range
        infinite_coords = set()
        outter_bounds = [itertools.product(range(min_x - 1, max_x + 2), (min_y - 1, max_y + 1)),
                         itertools.product((min_x - 1, max_x + 1), range(min_y, max_y + 1))]
        for products in outter_bounds:
            for x_coord, y_coord in products:
                closet_coords = get_closet_coords(
                    coords_list, x_coord, y_coord)
                if len(closet_coords) == 1 and closet_coords[0] not in infinite_coords:
                    infinite_coords.add(closet_coords[0])

        # count total regions with optimal total distance
        total_region = 0
        for x_coord in range(min_x, max_x + 1):
            for y_coord in range(min_y, max_y + 1):
                total = get_distance_total(
                    coords_list, x_coord, y_coord)
                if total:
                    total_region += 1

        print(total_region)


if __name__ == "__main__":
    main()
