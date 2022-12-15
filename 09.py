from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def should_move(self, other) -> bool:
        return abs(self.x - other.x) > 1 or abs(self.y - other.y) > 1

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def move(self, direction):
        return {
            "U": self + Position(0, 1),
            "D": self + Position(0, -1),
            "L": self + Position(-1, 0),
            "R": self + Position(1, 0),
        }[direction]


if __name__ == '__main__':
    with open("inputs/9.txt", "r") as f:
        data_in = f.readlines()
    parsed = [
        (row.split(" ")[0], int(row.split(" ")[1]))
        for row in data_in
    ]
    new_head = tail = Position(0, 0)
    visited = {tail}
    for direction, iterations in parsed:
        for _ in range(iterations):
            old_head = new_head
            new_head = new_head.move(direction)
            if new_head.should_move(tail):
                tail = old_head
                visited.add(tail)
    print(len(visited))


