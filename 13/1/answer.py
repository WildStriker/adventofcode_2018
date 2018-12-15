import typing


class Cart:
    DIRECTIONS = {
        'UP': 0,
        'DOWN': 0.5,
        'LEFT': 0.75,
        'RIGHT': 0.25,
        'CRASH': -1
    }

    DIRECTION_CHARACTERS = {
        0: '^',
        0.5: 'v',
        0.75: '<',
        0.25: '>',
        -1: 'X'
    }

    INTERSECTION_TURNS = (0.75,
                          0, 0.25)

    def __init__(self, character, coords, tracks: typing.Dict[tuple, 'Track']):
        for direction, direction_chatacter in Cart.DIRECTION_CHARACTERS.items():
            if character == direction_chatacter:
                self._direction = direction

        self._coords = coords
        self._tracks = tracks
        self._next_intersection_turn = self.intersection_turn()

    @property
    def character(self):
        return Cart.DIRECTION_CHARACTERS[self._direction]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @property
    def coords(self):
        return self._coords

    def intersection_turn(self):
        while True:
            for turn in Cart.INTERSECTION_TURNS:
                new_direction = self._direction + turn
                yield new_direction % 1

    def move_cart(self) -> bool:
        # get new coords
        track: Track = self._tracks[self._coords]
        track.cart = None
        new_coords = self._coords
        if self._direction == Cart.DIRECTIONS['UP']:
            new_coords = (new_coords[0], new_coords[1] - 1)
        elif self._direction == Cart.DIRECTIONS['DOWN']:
            new_coords = (new_coords[0], new_coords[1] + 1)
        elif self._direction == Cart.DIRECTIONS['LEFT']:
            new_coords = (new_coords[0] - 1, new_coords[1])
        elif self._direction == Cart.DIRECTIONS['RIGHT']:
            new_coords = (new_coords[0] + 1, new_coords[1])
        self._coords = new_coords

        new_track: Track = self._tracks[self._coords]
        # check for collisions
        if new_track.cart:
            self._direction = Cart.DIRECTIONS['CRASH']
            new_track.cart.direction = Cart.DIRECTIONS['CRASH']
            return True
        else:
            new_track.cart = self

        # turn at intersection
        if new_track.character == Track.CHARACTERS['INTERSECTION']:
            self._direction = next(self._next_intersection_turn)
        # turn at corners
        elif self._direction == Cart.DIRECTIONS['UP']:
            if new_track.character == Track.CHARACTERS['UP_RIGHT']:
                self._direction = Cart.DIRECTIONS['LEFT']
            elif new_track.character == Track.CHARACTERS['UP_LEFT']:
                self._direction = Cart.DIRECTIONS['RIGHT']
        elif self._direction == Cart.DIRECTIONS['DOWN']:
            if new_track.character == Track.CHARACTERS['DOWN_RIGHT']:
                self._direction = Cart.DIRECTIONS['LEFT']
            elif new_track.character == Track.CHARACTERS['DOWN_LEFT']:
                self._direction = Cart.DIRECTIONS['RIGHT']
        elif self._direction == Cart.DIRECTIONS['LEFT']:
            if new_track.character == Track.CHARACTERS['UP_LEFT']:
                self._direction = Cart.DIRECTIONS['DOWN']
            elif new_track.character == Track.CHARACTERS['DOWN_LEFT']:
                self._direction = Cart.DIRECTIONS['UP']
        elif self._direction == Cart.DIRECTIONS['RIGHT']:
            if new_track.character == Track.CHARACTERS['UP_RIGHT']:
                self._direction = Cart.DIRECTIONS['DOWN']
            elif new_track.character == Track.CHARACTERS['DOWN_RIGHT']:
                self._direction = Cart.DIRECTIONS['UP']

        return False


class Track:
    CHARACTERS = {
        'INTERSECTION': '+',
        'UP_DOWN': '|',

        'LEFT_RIGHT': '-',
        'UP_LEFT': '/',

        'UP_RIGHT': '\\',

        'DOWN_LEFT': '\\',
        'DOWN_RIGHT': '/'
    }

    def __init__(self, character, cart: Cart = None):
        self._character = character
        self._cart = cart

    @property
    def character(self):
        return self._character

    @property
    def cart(self) -> Cart:
        return self._cart

    @cart.setter
    def cart(self, cart):
        self._cart = cart


def set_up(file_input):
    cart_to_track = {
        Cart.DIRECTION_CHARACTERS[0]: Track.CHARACTERS['UP_DOWN'],
        Cart.DIRECTION_CHARACTERS[0.5]: Track.CHARACTERS['UP_DOWN'],
        Cart.DIRECTION_CHARACTERS[0.75]: Track.CHARACTERS['LEFT_RIGHT'],
        Cart.DIRECTION_CHARACTERS[0.25]: Track.CHARACTERS['LEFT_RIGHT']
    }
    carts = []
    tracks = {}
    for y_coord, line in enumerate(file_input):
        for x_coord, character in enumerate(line):
            coords = (x_coord, y_coord)
            if character in Track.CHARACTERS.values():
                # create track
                track = Track(character)
                tracks[coords] = track
            elif character in Cart.DIRECTION_CHARACTERS.values():
                # create cart and track
                cart = Cart(character, coords, tracks)
                carts.append(cart)
                track = Track(cart_to_track[character], cart)
                tracks[coords] = track
    return carts


def compare_cart(cart: Cart):
    return cart.coords[1], cart.coords[0]


def get_crash(carts: typing.List[Cart]):
    while True:
        carts.sort(key=compare_cart)
        for cart in carts:
            has_crashed = cart.move_cart()
            if has_crashed:
                return cart.coords


def main():
    with open('inputs\\input13.txt') as file_input:
        carts = set_up(file_input)

    crash_coords = get_crash(carts)

    print(crash_coords)


if __name__ == "__main__":
    main()
