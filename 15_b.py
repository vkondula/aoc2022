from __future__ import annotations

import re
from typing import NamedTuple, Optional


class Line(NamedTuple):
    a: Point
    b: Point

    def get_intersection(self, other: Line) -> Optional[Point]:
        x_diff = (self.a.x - self.b.x, other.a.x - other.b.x)
        y_diff = (self.a.y - self.b.y, other.a.y - other.b.y)
        div = (x_diff[0] * y_diff[1] - y_diff[0] * x_diff[1])
        if div == 0:
            return None

        d = (self.a.x * self.b.y - self.b.x * self.a.y, other.a.x * other.b.y - other.b.x * other.a.y)
        x = (d[0] * x_diff[1] - d[1] * x_diff[0]) // div
        y = (d[0] * y_diff[1] - d[1] * y_diff[0]) // div

        return Point(x, y)

    def candidates(self, other: Line, limit: int):
        if (point := self.get_intersection(other)) is None:
            return set()
        return {
            Point(point.x + x, point.y + y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if 0 <= point.x + x <= limit and 0 <= point.y + y <= limit
        }


class Point(NamedTuple):
    x: int
    y: int
    beacon: Optional[Point] = None

    def diff(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def size(self):
        return abs(self.x - self.beacon.x) + abs(self.y - self.beacon.y)

    def lines(self):
        size = self.size()
        lines = []
        for start in (Point(self.x - size - 1, self.y), Point(self.x + size + 1, self.y)):
            for end in (Point(self.x, self.y - size - 1), Point(self.x, self.y + size + 1)):
                lines.append(Line(start, end))
        return lines


if __name__ == '__main__':
    with open("inputs/15.txt", "r") as f:
        data_in = f.readlines()
    line_groups = []
    senzors = []
    for row in data_in:
        match = re.search(r"x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", row)
        beacon = Point(int(match.group(3)), int(match.group(4)))
        senzor = Point(int(match.group(1)), int(match.group(2)), beacon)
        senzors.append(senzor)
        line_groups.append(senzor.lines())
    candidates = set()
    for i in range(len(line_groups)):
        for j in range(i + 1, len(line_groups)):
            for self_line in line_groups[i]:
                for other_line in line_groups[j]:
                    if tmp := self_line.candidates(other_line, 4000000):
                        candidates |= tmp
    for candidate in candidates:
        for senzor in senzors:
            if senzor.diff(candidate) <= senzor.size():
                break
        else:
            print(candidate)
            print(candidate.x * 4000000 + candidate.y)
            break
