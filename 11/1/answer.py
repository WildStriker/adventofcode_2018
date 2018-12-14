
def get_power_level(x_coord, y_coord, serial, fuel_cell_size) -> int:
    total_power_level = 0
    for x_offset in range(x_coord, x_coord + fuel_cell_size[0]):
        for y_offset in range(y_coord, y_coord + fuel_cell_size[1]):
            rack_id = x_offset + 10
            power_level = rack_id * y_offset
            power_level += serial
            power_level *= rack_id
            power_level = power_level // 100 % 10
            power_level -= 5
            total_power_level += power_level
    return total_power_level


def get_highest_grid_level(serial, fuel_cell_size=(3, 3), grid_size=(300, 300)):
    coord = None
    highest_power_level = None
    for x_coord in range(1, grid_size[0] - fuel_cell_size[0] + 2):
        for y_coord in range(1, grid_size[1] - fuel_cell_size[1] + 2):
            power_level = get_power_level(
                x_coord, y_coord, serial, fuel_cell_size)
            if highest_power_level is None or power_level > highest_power_level:
                coord = (x_coord, y_coord)
                highest_power_level = power_level
    return coord, highest_power_level


def main():
    with open('inputs\\input11.txt') as input_file:
        serial = int(input_file.read())
        coord, power_level = get_highest_grid_level(serial)

        print(f'Coords: {coord}\npower level: {power_level}')


if __name__ == "__main__":
    main()
