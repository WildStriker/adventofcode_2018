import re
import typing


class Point:
    min_x = None
    max_x = None

    min_y = None
    max_y = None

    def __init__(self, position: tuple, velocity: tuple):
        self._position = position

        self.update_range()

        self._velocity = velocity

    @property
    def position(self):
        return self._position

    def add_velocity(self):
        self._position = (self._position[0] + self._velocity[0],
                          self._position[1] + self._velocity[1])

        self.update_range()

    def update_range(self):
        position_x = self.position[0]
        position_y = self.position[1]
        if Point.min_x is None or position_x < Point.min_x:
            Point.min_x = position_x
        if Point.max_x is None or position_x > Point.max_x:
            Point.max_x = position_x
        if Point.min_y is None or position_y < Point.min_y:
            Point.min_y = position_y
        if Point.max_y is None or position_y > Point.max_y:
            Point.max_y = position_y


def get_initial_values(file_input) -> (typing.List[Point], set):
    pattern = 'position=< *(-*[0-9]+), *(-*[0-9]+)> velocity=< *(-*[0-9]+), *(-*[0-9]+)>'
    points = []
    points_set = set()
    for line in file_input:
        match = re.match(pattern, line)

        position = (int(match.group(1)), int(match.group(2)))
        velocity = (int(match.group(3)), int(match.group(4)))

        points.append(Point(position, velocity))
        points_set.add(position)

    return points, points_set


def draw_points(points_set: set):
    # draw graph
    for position_y in range(Point.min_y, Point.max_y + 1):
        line = []
        for position_x in range(Point.min_x, Point.max_x + 1):
            coords = (position_x, position_y)
            if coords in points_set:
                line.append('#')
            else:
                line.append('.')
        print(' '.join(line))


def add_velocity(points: typing.List[Point]) -> set:
    # allow graph to resize
    Point.min_x = None
    Point.max_x = None
    Point.min_y = None
    Point.max_y = None

    points_set = set()
    for point in points:
        point.add_velocity()
        points_set.add(point.position)

    return points_set


def main():
    with open('inputs\\input10.txt') as file_input:
        points, points_set = get_initial_values(file_input)

        print("Enter Limit, if range is larger than don't print")
        total_x = int(input('Total max X:'))
        total_y = int(input('Total max Y:'))

        second_count = 0
        try:
            while True:
                if Point.max_x - Point.min_x + 1 < total_x and \
                        Point.max_y - Point.min_y + 1 < total_y:
                    print(f'\n\nSecond: {second_count}\nMessage:')
                    draw_points(points_set)
                    input('Enter to Continue')
                points_set = add_velocity(points)
                second_count += 1
        except KeyboardInterrupt:
            print('Exiting..')

if __name__ == "__main__":
    main()
