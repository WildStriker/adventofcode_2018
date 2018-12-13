import typing
import re


class Guard:
    def __init__(self, guard_id):
        self._guard_id = guard_id

        self._minute_sleep_count = {}
        self._total_minutes = 0
        self._minute_most_asleep = None

    def add_sleep_range(self, start, stop):
        stop += 1
        for minute in range(start, stop):
            self._total_minutes += 1
            minute_sleep = self._minute_sleep_count.get(minute, 0)
            minute_sleep += 1
            self._minute_sleep_count[minute] = minute_sleep

            if not self._minute_most_asleep or \
                    minute_sleep > self._minute_sleep_count[self.minute_most_asleep]:
                self._minute_most_asleep = minute

    @property
    def total_minutes(self):
        return self._total_minutes

    @property
    def minute_most_asleep(self):
        return self._minute_most_asleep

    @property
    def guard_id(self):
        return self._guard_id


def get_sleep_range(log) -> typing.Tuple[int, int, int]:
    log_start = 19
    guard_end = 24
    asleep_end = 31
    awake_end = 27
    minute_start = 15
    minute_end = 17
    for line in log:
        if line[log_start:guard_end] == 'Guard':
            match = re.search('#([0-9]+)', line)
            guard_id = int(match.group(1))
        elif line[log_start:asleep_end] == 'falls asleep':
            start = int(line[minute_start:minute_end])
        elif line[log_start:awake_end] == 'wakes up':
            stop = int(line[minute_start:minute_end])
            yield guard_id, start, stop


def get_guard_most(log) -> Guard:
    guards: typing.Dict[int, Guard] = {}
    guard_most_sleep: Guard = None

    for guard_id, start, stop in get_sleep_range(log):
        if guard_id in guards:
            guard = guards[guard_id]
        else:
            guard = Guard(guard_id)
            guards[guard_id] = guard

        guard.add_sleep_range(start, stop)

        if not guard_most_sleep or guard.total_minutes > guard_most_sleep.total_minutes:
            guard_most_sleep = guard

    return guard_most_sleep


def main():
    with open('inputs\\input04.txt') as input_file:
        log = sorted(input_file)

    guard = get_guard_most(log)

    answer = guard.guard_id * guard.minute_most_asleep
    print(f'{guard.guard_id} * {guard.minute_most_asleep} = {answer}')


if __name__ == "__main__":
    main()
