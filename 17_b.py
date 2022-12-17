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


class Cycle:
    def __init__(self, data):
        self.next_index = 0
        self.size = len(data)
        self.data = data

    def next(self):
        prev = self.next_index
        self.next_index = (self.next_index + 1) % self.size
        return self.data[prev]


class Shape:
    def __init__(self, raw, index):
        self.points = {
            (x + 2, y)
            for y, line in enumerate(raw)
            for x, item in enumerate(line)
            if item == "#"
        }
        self.index = index

    def spawn(self, height):
        return {(x, y + height) for x, y in self.points}


class Game:
    def __init__(self, commands_generator):
        self.size = 7
        self.full = set()
        self.height = 0
        self.shapes = Cycle([Shape(raw, i) for i, raw in enumerate(SHAPES)])
        self.commands = commands_generator
        self.count = 0
        self.snapshots = {}

    def move(self, points, offset=None):
        if not offset:
            offset = (1, 0) if self.commands.next() == ">" else (-1, 0)
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
        # if self.commands.next_index == 0 and self.shapes.next_index == 0 and self.height > 0:
        #     print("now")
        shape = self.shapes.next()
        points = shape.spawn(self.height + 3)
        end = False
        while not end:
            points, _ = self.move(points)
            points, end = self.move(points, (0, -1))
        self.full |= points
        self.height = max(self.height, *(y + 1 for _, y in points))
        if shape.index == 0 and len([_ for x, _ in points if 1 <= x < 5]) == 4:
            if self.commands.next_index in self.snapshots:
                height_diff = self.height - self.snapshots[self.commands.next_index][0]
                count_diff = self.count - self.snapshots[self.commands.next_index][1]
                times = (1000000000000 - 1 - self.count) // count_diff
                self.count += count_diff * times
                self.height += height_diff * times
                self.full = {(x, y + height_diff * times) for x, y in self.full}

            self.snapshots[self.commands.next_index] = (self.height, self.count)

    def cleanup(self):
        self.full = {(x, y) for x, y in self.full if y > self.height - 1000}


if __name__ == '__main__':
    with open("inputs/17.txt", "r") as f:
        data_in = f.read().strip("\n")
    game = Game(Cycle(data_in))
    while game.count < 1000000000000:
        game.round()
        game.count += 1
        if game.count % 10000 == 0:
            game.cleanup()
    print(game.height)
