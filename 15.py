import re
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def diff(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def scanned(self, other):
        diff = self.diff(other)
        retval = set()
        for y in range(2000000, 2000001):
            for x in range(self.x - diff, self.x + diff + 1):
                if Point(x, y) == other:
                    continue
                if self.diff(Point(x, y)) <= diff:
                    retval.add((x, y))
        return retval


if __name__ == '__main__':
    with open("inputs/15.txt", "r") as f:
        data_in = f.readlines()
    scanned = set()
    for row in data_in:
        match = re.search(r"x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", row)
        scanned |= Point(int(match.group(1)), int(match.group(2))).scanned(
            Point(int(match.group(3)), int(match.group(4)))
        )
    print(len([a for a in scanned if a[1] == 2000000]))
