import attr
from math import lcm

DIRECTION_MAPPING = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def rotate(record: (int, int)):
    return ((record[0] - 1) % (MAX_X - 2)) + 1, ((record[1] - 1) % (MAX_Y - 2)) + 1


def get_next_blizzards(blizzards):
    retval = [set() for _ in range(4)]
    for i, direction in enumerate(blizzards):
        diff = DIRECTION_MAPPING[i]
        for record in direction:
            retval[i].add(rotate(add(record, diff)))
    return retval


GLOBAL_MAX = 10000
MAX_X = 1000
MAX_Y = 1000
VISITED = {}


@attr.s(auto_attribs=True)
class Snapshot:
    turn: int
    location: (int, int)
    walls: set[(int, int)]
    blizzards: list[set[(int, int)]]
    end: (int, int)

    def action(self):
        global GLOBAL_MAX, VISITED
        signature = *self.location, self.turn % len(self.blizzards)
        if VISITED.get(signature, 1000) <= self.turn:
            return []
        VISITED[signature] = self.turn
        if self.turn > GLOBAL_MAX:
            return []
        occupied = self.walls | self.blizzards[(self.turn + 1) % len(self.blizzards)]
        retval = []
        for diff in DIRECTION_MAPPING + [(0, 0)]:
            new_location = add(self.location, diff)
            if new_location == self.end:
                GLOBAL_MAX = min(self.turn + 1, GLOBAL_MAX)
            if new_location not in occupied:
                retval.append(
                    Snapshot(
                        self.turn + 1,
                        new_location,
                        self.walls,
                        self.blizzards,
                        self.end,
                    )
                )
        return retval

    def dump(self):
        print(f"=== {self.turn} ===")
        for i in range(MAX_Y):
            retval = []
            for j in range(MAX_X):
                record =(j, i)
                if record == self.location:
                    retval.append("E")
                elif record in self.walls:
                    retval.append("#")
                elif record in self.blizzards[self.turn % len(self.blizzards)]:
                    retval.append("x")
                else:
                    retval.append(".")
            print("".join(retval))


def main():
    global MAX_Y, MAX_X, GLOBAL_MAX, VISITED
    with open("inputs/24.txt", "r") as f:
        data_in = f.read()
    data_in = data_in.replace("#.#", "#S#", 1).replace("#.#", "#E#", 1).split("\n")
    MAX_Y = len(data_in)
    MAX_X = len(data_in[0])
    walls = set()
    blizzards = [set() for _ in range(4)]
    start = None
    end = None
    for i, line in enumerate(data_in):
        for j, value in enumerate(line):
            location = (j, i)
            if value == "#":
                walls.add(location)
            if value in "<>^v":
                blizzards[">v<^".index(value)].add(location)
            if value == "S":
                start = location
            if value == "E":
                end = location
    walls |= {(i, -1) for i in range(3)}
    walls |= {(MAX_X - i, MAX_Y) for i in range(3)}
    dumped_blizzards = [set.union(*blizzards)]
    snap_blizzards = [blizzards]
    for i in range(lcm(MAX_Y - 2, MAX_X - 2) - 1):
        blizzard = get_next_blizzards(snap_blizzards[i])
        dumped_blizzards.append(set.union(*blizzard))
        snap_blizzards.append(blizzard)
    stack = [Snapshot(0, start, walls, dumped_blizzards, end)]
    while stack:
        snapshot = stack.pop(0)
        stack += snapshot.action()
    counter = GLOBAL_MAX
    GLOBAL_MAX, VISITED = 10000, {}
    stack = [Snapshot(counter, end, walls, dumped_blizzards, start)]
    while stack:
        snapshot = stack.pop(0)
        stack += snapshot.action()
    counter = GLOBAL_MAX
    GLOBAL_MAX, VISITED = 10000, {}
    stack = [Snapshot(counter, start, walls, dumped_blizzards, end)]
    while stack:
        snapshot = stack.pop(0)
        stack += snapshot.action()
    print(GLOBAL_MAX)


if __name__ == '__main__':
    main()
