
def calc_power_level(x_coord, y_coord, serial) -> int:
    rack_id = x_coord + 10
    power_level = rack_id * y_coord
    power_level += serial
    power_level *= rack_id
    power_level = power_level // 100 % 10
    power_level -= 5
    return power_level


def get_total_power_level(x_coord, y_coord, grid, cell_range):
    x_coord -= 1
    y_coord -= 1
    total_power_level = 0
    for x_offset in range(x_coord, x_coord + cell_range[0]):
        for y_offset in range(y_coord, y_coord + cell_range[1]):
            total_power_level += grid[x_offset][y_offset]
    return total_power_level


def get_highest_grid_level(serial, grid_size=300):

    grid = []
    for x_coord in range(1, grid_size + 1):
        y_list = []
        grid.append(y_list)
        for y_coord in range(1, grid_size + 1):
            y_list.append(calc_power_level(x_coord, y_coord, serial))

    coord = None
    highest_power_level = None
    highest_fuel_cell_size = None
    for x_coord in range(1, grid_size + 1):
        for y_coord in range(1, grid_size + 1):
            total_power_level = 0
            for fuel_cell_size in range(1, grid_size + 1):
                if fuel_cell_size + x_coord - 1 > grid_size or \
                        fuel_cell_size + y_coord - 1 > grid_size:
                    break
                if fuel_cell_size == 1:
                    cell_range = (1, 1)
                    total_power_level += get_total_power_level(
                        x_coord,
                        y_coord,
                        grid,
                        cell_range)
                else:
                    cell_range = (1, fuel_cell_size)
                    total_power_level += get_total_power_level(
                        x_coord + fuel_cell_size - 1,
                        y_coord,
                        grid,
                        cell_range)
                    cell_range = (fuel_cell_size - 1, 1)
                    total_power_level += get_total_power_level(
                        x_coord,
                        y_coord + fuel_cell_size - 1,
                        grid,
                        cell_range)
                if highest_power_level is None or total_power_level > highest_power_level:
                    coord = (x_coord, y_coord)
                    highest_power_level = total_power_level
                    highest_fuel_cell_size = fuel_cell_size
    return coord, highest_power_level, highest_fuel_cell_size


def main():
    with open('inputs\\input11.txt') as input_file:
        serial = int(input_file.read())
        coord, power_level, fuel_size = get_highest_grid_level(serial)

        print(
            f'Coords: {coord}\npower level: {power_level}\nfuel size: {fuel_size}')


if __name__ == "__main__":
    main()
