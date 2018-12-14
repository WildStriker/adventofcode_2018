import re
import collections


def get_gamedata(data):
    pattern = r'([0-9]+) players; last marble is worth ([0-9]+) points'

    match = re.match(pattern, data)
    if match:
        return int(match.group(1)), int(match.group(2))


def get_highscore(player_count, highest_marble) -> int:

    players = {}
    played_marble = 0
    played_marbles = collections.deque([0])
    for played_marble in range(1, highest_marble + 1):
        if played_marble % 23 == 0:
            player_number = played_marble % player_count
            played_marbles.rotate(7)
            score = played_marbles.pop() + played_marble
            players[player_number] = players.get(player_number, 0) + score
            played_marbles.rotate(-1)
        else:
            played_marbles.rotate(-1)
            played_marbles.append(played_marble)

    return max(players.values())


def main():
    with open('inputs\\input09.txt') as input_file:
        player_count, highest_marble = get_gamedata(input_file.read())
        highscore = get_highscore(player_count, highest_marble * 100)
        print(highscore)


if __name__ == "__main__":
    main()
