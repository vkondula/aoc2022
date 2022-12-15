from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def should_move(self, other):
        if abs(self.x - other.x) > 1:
            return Position(self.x + int((other.x - self.x) * 0.5), other.y - int((other.y - self.y) * 0.5))
        if abs(self.y - other.y) > 1:
            return Position(other.x - int((other.x - self.x) * 0.5), self.y + int((other.y - self.y) * 0.5))
        return None

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
    snake = [Position(0, 0) for _ in range(10)]
    visited = {snake[9]}
    for direction, iterations in parsed:
        for _ in range(iterations):
            snake[0] = snake[0].move(direction)
            for i in range(1, 10):
                if new_position := snake[i].should_move(snake[i - 1]):
                    snake[i] = new_position
            visited.add(snake[9])
    print(len(visited))


