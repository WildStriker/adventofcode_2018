def main():
    with open('inputs\\input22.txt') as input_file:
        depth = int(input_file.readline().split(':')[1])
        target_x, target_y = map(
            int, input_file.readline().split(':')[1].split(','))
    target = (target_x, target_y)

    cave = {}
    risk = 0
    for x_coord in range(target_x + 1):
        for y_coord in range(target_y + 1):
            coords = (x_coord, y_coord)
            if coords == target or coords == (0, 0):
                index = 0
            elif y_coord == 0:
                index = x_coord * 16807
            elif x_coord == 0:
                index = y_coord * 48271
            else:
                left_coords = (coords[0] - 1, coords[1])
                up_coords = (coords[0], coords[1]-1)
                index = cave[left_coords]['erosion'] * \
                    cave[up_coords]['erosion']

            cave[coords] = region = {}
            region['index'] = index
            erosion = (index + depth) % 20183
            region['erosion'] = erosion
            region_type = erosion % 3
            region['type'] = region_type

            risk += region_type

    print(risk)


if __name__ == "__main__":
    main()
