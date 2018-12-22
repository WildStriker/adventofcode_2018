import queue


def manhattan_distance(coords_1, coords_2):
    return abs(coords_1[0] - coords_2[0]) + abs(coords_1[1] - coords_2[1])


def get_neighbors(y_pos, x_pos, cave):
    neighbors = []
    # up
    up_coord = (y_pos-1, x_pos)
    if up_coord in cave:
        neighbors.append(up_coord)

    # left
    left_coord = (y_pos, x_pos - 1)
    if left_coord in cave:
        neighbors.append(left_coord)

    # right
    right_coord = (y_pos, x_pos + 1)
    if right_coord in cave:
        neighbors.append(right_coord)

    # down
    down_coord = (y_pos+1, x_pos)
    if down_coord in cave:
        neighbors.append(down_coord)

    return neighbors


def a_star(start, goal, cave):
    torch = 0
    climbling_gear = 1
    nothing = 2

    rocky = 0
    wet = 1
    narrow = 2

    frontier = queue.PriorityQueue()
    start_gear = (start, torch)
    frontier.put((0, start_gear))

    came_from = {
        start_gear: None
    }
    cost_so_far = {
        start_gear: 0
    }

    while not frontier.empty():
        _, current = frontier.get()

        if current[0] == goal:
            break

        current_gear = current[1]
        current_region = cave[current[0]]['type']
        neighbors_gear = []
        for neighbor in get_neighbors(current[0][0], current[0][1], cave):
            new_region_type = cave[neighbor]['type']
            if neighbor == goal:
                if current_gear != torch:
                    weight = 8
                else:
                    weight = 1
                neighbors_gear.append(((neighbor, torch), weight))
            elif new_region_type == rocky and current_gear not in (climbling_gear, torch):
                weight = 8
                if current_region == wet:
                    neighbors_gear.append(((neighbor, climbling_gear), weight))
                else:
                    neighbors_gear.append(((neighbor, torch), weight))
            elif new_region_type == wet and current_gear not in (climbling_gear, nothing):
                weight = 8
                if current_region == rocky:
                    neighbors_gear.append(((neighbor, climbling_gear), weight))
                else:
                    neighbors_gear.append(((neighbor, nothing), weight))
            elif new_region_type == narrow and current_gear not in (torch, nothing):
                weight = 8
                if current_region == rocky:
                    neighbors_gear.append(((neighbor, torch), weight))
                else:
                    neighbors_gear.append(((neighbor, nothing), weight))
            else:
                weight = 1
                neighbors_gear.append(((neighbor, current_gear), weight))

        for neighbor_gear, weight in neighbors_gear:

            new_cost = cost_so_far[current] + weight
            if neighbor_gear not in cost_so_far or new_cost < cost_so_far[neighbor_gear]:
                cost_so_far[neighbor_gear] = new_cost
                priority = new_cost + \
                    manhattan_distance(goal, neighbor_gear[0])
                frontier.put((priority, neighbor_gear))
                came_from[neighbor_gear] = current

    if (goal, torch) not in came_from:
        return None

    return cost_so_far[(goal, torch)]


def main():
    with open('inputs\\input22.txt') as input_file:
        depth = int(input_file.readline().split(':')[1])
        target_x, target_y = map(
            int, input_file.readline().split(':')[1].split(','))
    target = (target_y, target_x)

    cave = {}
    for x_coord in range(target_x + 51):
        for y_coord in range(target_y + 51):
            coords = (y_coord, x_coord)
            if coords == target or coords == (0, 0):
                index = 0
            elif y_coord == 0:
                index = x_coord * 16807
            elif x_coord == 0:
                index = y_coord * 48271
            else:
                left_coords = (coords[0], coords[1] - 1)
                up_coords = (coords[0]-1, coords[1])
                index = cave[left_coords]['erosion'] * \
                    cave[up_coords]['erosion']

            cave[coords] = region = {}
            region['index'] = index
            erosion = (index + depth) % 20183
            region['erosion'] = erosion
            region_type = erosion % 3
            region['type'] = region_type

    time_cost = a_star((0, 0), target, cave)

    print(time_cost)


if __name__ == "__main__":
    main()
