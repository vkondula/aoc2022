from itertools import cycle

SHAPES = [
    ["####"],
    [
        ".#.",
        "###",
        ".#."
    ],
    [
        "###",
        "..#",
        "..#"
    ],
    [
        "#",
        "#",
        "#",
        "#"
    ],
    [
        "##",
        "##"
    ]
]


class Shape:
    def __init__(self, raw):
        self.points = {
            (x + 2, y)
            for y, line in enumerate(raw)
            for x, item in enumerate(line)
            if item == "#"
        }

    def spawn(self, height):
        return {(x, y + height) for x, y in self.points}


class Game:
    def __init__(self, commands_generator):
        self.size = 7
        self.full = set()
        self.height = 0
        self.shapes = cycle([Shape(raw) for raw in SHAPES])
        self.commands = commands_generator
        self.count = 0

    def move(self, points, offset=None):
        if not offset:
            offset = (1, 0) if next(self.commands) == ">" else (-1, 0)
        new_points = {(x + offset[0], y + offset[1]) for x, y in points}
        if self.overlaps(new_points):
            return points, True
        return new_points, False

    def overlaps(self, points):
        for x, y in points:
            if x < 0 or x >= self.size or y < 0:
                return True
        return bool(self.full & points)

    def round(self):
        shape = next(self.shapes)
        points = shape.spawn(self.height + 3)
        end = False
        while not end:
            points, _ = self.move(points)
            points, end = self.move(points, (0, -1))
        self.full |= points
        self.height = max(self.height, *(y + 1 for _, y in points))


def print_p(points):
    height = max(*(y for x, y in points))
    for y in range(height, -1, -1):
        print("".join(["#" if (x, y) in points else "." for x in range(7)]))
    print("")


if __name__ == '__main__':
    with open("inputs/17.txt", "r") as f:
        data_in = f.read().strip("\n")
    game = Game(cycle(data_in))
    for _ in range(2022):
        game.round()
    print(game.height)
