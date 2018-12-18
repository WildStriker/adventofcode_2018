import queue
import typing


class Unit:
    CHARACTER = 'U'

    def __init__(self, coords: tuple, attack_power=3, hitpoints=200):
        self._coords = coords
        self._attack_power = attack_power
        self._hitpoints = hitpoints

    @property
    def attack_power(self):
        return self._attack_power

    @property
    def hitpoints(self):
        return self._hitpoints

    @hitpoints.setter
    def hitpoints(self, hitpoints):
        self._hitpoints = hitpoints

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, coords):
        if self.manhattan_distance(self._coords, coords) == 1:
            self._coords = coords
        else:
            raise ValueError('Unable to move to this coordinate!')

    def manhattan_distance(self, coords_1, coords_2):
        return abs(coords_1[0] - coords_2[0]) + abs(coords_1[1] - coords_2[1])

    def attack(self, enemy: 'Unit'):
        if self.manhattan_distance(self._coords, enemy.coords) == 1 and enemy.hitpoints > 0:
            enemy.hitpoints -= self._attack_power
        else:
            raise ValueError('Unable to attack this unit')


class Goblin(Unit):
    CHARACTER = 'G'


class Elf(Unit):
    CHARACTER = 'E'


class Tile:
    CHARACTER = '*'

    def __init__(self, is_walkable, unit):
        self._is_walkable: bool = is_walkable
        self._unit: Unit = unit

    @property
    def unit(self) -> Unit:
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def is_walkable(self) -> bool:
        return self._is_walkable and not self._unit

    def display(self):
        if self._unit:
            return self._unit.CHARACTER
        else:
            return self.CHARACTER


class WallTile(Tile):
    CHARACTER = '#'

    def __init__(self):
        super().__init__(False, None)


class OpenCavernTile(Tile):
    CHARACTER = '.'

    def __init__(self, unit: Unit = None):
        super().__init__(True, unit)


class Map:
    def __init__(self, file, elves_attack_power):
        self._elves: typing.Set[Elf] = None
        self._goblins: typing.Set[Goblin] = None
        self._tiles: typing.Dict[tuple, Tile] = None
        self._last_coord = None
        self._full_round_count = None

        self._elf_count = 0
        self._elves_attack_power = elves_attack_power
        self._file = file
        self.setup()

    def setup(self):
        self._elves = set()
        self._goblins = set()
        self._tiles = {}
        y_coord = None
        max_x = 0
        with open(self._file) as input_file:
            for y_coord, line in enumerate(input_file):
                for x_coord, character in enumerate(line):
                    coords = (y_coord, x_coord)
                    if character == WallTile.CHARACTER:
                        self._tiles[coords] = WallTile()
                    elif character == OpenCavernTile.CHARACTER:
                        self._tiles[coords] = OpenCavernTile()
                    elif character == Goblin.CHARACTER:
                        goblin = Goblin(coords)
                        self._goblins.add(goblin)
                        self._tiles[coords] = OpenCavernTile(goblin)
                    elif character == Elf.CHARACTER:
                        elf = Elf(coords, self._elves_attack_power)
                        self._elves.add(elf)
                        self._tiles[coords] = OpenCavernTile(elf)
                    if x_coord > max_x and character != '\n':
                        max_x = x_coord
        self._last_coord = (y_coord, max_x)
        self._elf_count = len(self._elves)

    @property
    def full_round_count(self):
        return self._full_round_count

    def show_map(self):
        max_y, max_x = self._last_coord
        for y_coord in range(max_y + 1):
            hitpoints_remaning = []
            output = ''
            for x_coord in range(max_x + 1):
                coords = (y_coord, x_coord)
                tile: Tile = self._tiles[coords]
                output += tile.display()
                if tile.unit:
                    hitpoints_remaning.append(
                        f'{tile.unit.CHARACTER}({tile.unit.hitpoints})')

            print(output + '  ' + ', '.join(hitpoints_remaning))

    @staticmethod
    def move_order(unit: Unit):
        return unit.coords

    def power_to_win(self) -> int:
        while self._goblins:
            for _ in self.next_round():
                # an elf didn't survive increase atack and try again
                if self._elf_count != len(self._elves):
                    self._elves_attack_power += 1
                    self.setup()
                    break
        return self._elves_attack_power

    def next_round(self):
        round_count = 0
        while self._goblins and self._elves:
            round_count += 1
            self._full_round_count = round_count

            move_list: typing.List[Unit] = list(
                self._goblins) + list(self._elves)
            move_list.sort(key=Map.move_order)

            for unit in move_list:
                if unit.hitpoints > 0:
                    if isinstance(unit, Goblin):
                        enemy_units = self._elves
                    else:
                        enemy_units = self._goblins

                    # not a full round is n enemys left
                    if not enemy_units:
                        self._full_round_count = round_count - 1
                        break

                    killed: Unit = self.next_move(unit, enemy_units)
                    if killed:
                        if killed.coords in self._tiles:
                            self._tiles[killed.coords].unit = None
                        if isinstance(killed, Goblin) and killed in self._goblins:
                            self._goblins.remove(killed)
                        elif isinstance(killed, Elf) and killed in self._elves:
                            self._elves.remove(killed)
            yield round_count

    def get_near_target(self, unit: Unit, enemy_units: typing.Set[Unit]):
        target: Unit = None
        lowest_hp = None
        # check if unit is already in range
        for coords in self.get_neighbors(unit.coords[0], unit.coords[1]):
            near_unit = self._tiles[coords].unit
            if near_unit in enemy_units and (not lowest_hp or near_unit.hitpoints < lowest_hp):
                lowest_hp = near_unit.hitpoints
                target = near_unit
        return target

    def next_move(self, unit: Unit, enemy_units: typing.Set[Unit]):

        move = None
        target: Unit = self.get_near_target(unit, enemy_units)

        if not target:
            # get coords in range of enemy units
            move_list = []
            for enemy_unit in enemy_units:
                moves = self.dijkstra(unit.coords, enemy_unit.coords)
                if moves:
                    move_list.append((moves, enemy_unit))

            # filter to nearest enemy unit to move to
            if move_list:
                move_list.sort(key=lambda moves: (
                    len(moves[0]), moves[1].coords))
                moves, enemy_unit = move_list[0]

                move = moves.pop()

                self._tiles[unit.coords].unit = None
                unit.coords = move
                self._tiles[unit.coords].unit = unit

                # if no moves left then target enemy
                if not moves:
                    target = self.get_near_target(unit, enemy_units)

        # if in range attack will connect
        if target:
            unit.attack(target)
            if target.hitpoints <= 0:
                return target

        return None

    def total_health(self):
        total = 0
        for unit in self._elves:
            total += unit.hitpoints

        for unit in self._goblins:
            total += unit.hitpoints
        return total
    # ----PATH FINDING----

    def get_neighbors(self, y_pos, x_pos):
        neighbors = []
        # up
        up_coord = (y_pos-1, x_pos)
        if y_pos > 0:
            neighbors.append(up_coord)

        # left
        left_coord = (y_pos, x_pos - 1)
        if x_pos > 0:
            neighbors.append(left_coord)

        # right
        right_coord = (y_pos, x_pos + 1)
        if x_pos < self._last_coord[1]:
            neighbors.append(right_coord)

        # down
        down_coord = (y_pos+1, x_pos)
        if y_pos < self._last_coord[0]:
            neighbors.append(down_coord)

        return neighbors

    def dijkstra(self, start, goal):
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
            for neighbor in self.get_neighbors(current[0], current[1]):
                if self._tiles[neighbor].is_walkable:
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

        path = []
        current_path = came_from[goal]
        while current_path != start:
            path.append(current_path)
            current_path = came_from[current_path]
        return path


def main():
    area_map = Map('inputs\\input15.txt', 4)

    attack_power = area_map.power_to_win()

    print(attack_power)

    full_round_count = area_map.full_round_count
    total_health = area_map.total_health()
    outcome = total_health * full_round_count
    print(f'{full_round_count} * {total_health} = {outcome}')

if __name__ == "__main__":
    main()
