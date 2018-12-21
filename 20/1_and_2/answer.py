import queue


def get_neighbors(y_pos, x_pos):
    neighbors = []
    # up
    up_coord = (y_pos-1, x_pos)
    neighbors.append(up_coord)

    # left
    left_coord = (y_pos, x_pos - 1)
    neighbors.append(left_coord)

    # right
    right_coord = (y_pos, x_pos + 1)
    neighbors.append(right_coord)

    # down
    down_coord = (y_pos+1, x_pos)
    neighbors.append(down_coord)

    return neighbors


def dijkstra_door_count(grid, start, goal):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))

    came_from = {
        start: None
    }
    cost_so_far = {
        start: 0
    }

    while not frontier.empty():
        _, current = frontier.get()

        if current == goal:
            break

        neighbors = []
        for neighbor in get_neighbors(current[0], current[1]):
            if neighbor in grid:
                neighbors.append(neighbor)
            elif neighbor == goal:
                neighbors = [goal]
                break

        weight = 1
        for neighbor in neighbors:
            new_cost = cost_so_far[current] + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                frontier.put((priority, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return None

    door_count = 1
    current_path = came_from[goal]
    while current_path != start:
        if grid[current_path] != '.':
            door_count += 1
        current_path = came_from[current_path]
    return door_count


def directions(grid, start_coords, regex, index):
    coords = start_coords[:]
    while index < len(regex):
        character = regex[index]
        if character == 'N':
            coords = (coords[0] - 1, coords[1])
            grid[coords] = '-'
            coords = (coords[0] - 1, coords[1])
            grid[coords] = '.'
        elif character == 'E':
            coords = (coords[0], coords[1] + 1)
            grid[coords] = '|'
            coords = (coords[0], coords[1] + 1)
            grid[coords] = '.'
        elif character == 'S':
            coords = (coords[0] + 1, coords[1])
            grid[coords] = '-'
            coords = (coords[0] + 1, coords[1])
            grid[coords] = '.'
        elif character == 'W':
            coords = (coords[0], coords[1] - 1)
            grid[coords] = '|'
            coords = (coords[0], coords[1] - 1)
            grid[coords] = '.'
        elif character == '(':
            index = directions(grid, coords, regex, index + 1)
        elif character == '|':
            coords = start_coords[:]
        elif character == ')':
            return index

        index += 1

    return


def main():
    with open('inputs\\input20.txt') as input_file:
        regex = input_file.read()

    grid = {}
    directions(grid, (0, 0), regex[1:-1], 0)

    min_y = None
    max_y = None
    min_x = None
    max_x = None
    for coords in grid:
        if min_y is None or coords[0] < min_y:
            min_y = coords[0]
        if max_y is None or coords[0] > max_y:
            max_y = coords[0]

        if min_x is None or coords[1] < min_x:
            min_x = coords[1]
        if max_x is None or coords[1] > max_x:
            max_x = coords[1]

    for y_coord in range(min_y - 1, max_y + 2):
        line = ''
        for x_coord in range(min_x - 1, max_x + 2):
            coords = (y_coord, x_coord)
            if coords == (0, 0):
                line += 'X'
            else:
                line += grid.get(coords, '#')
        print(line)

    counts = []
    for coords in grid:
        if grid[coords] != '.':
            door_count = dijkstra_door_count(grid, (0, 0), coords)
            counts.append(door_count)

    print(sorted(counts, reverse=True)[0])
    filtered = len(list(filter(lambda count: count >= 1000, counts)))
    print(filtered)


if __name__ == "__main__":
    main()
