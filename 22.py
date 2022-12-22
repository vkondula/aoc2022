import re

FACING_MAPPING = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


if __name__ == '__main__':
    with open("inputs/22.txt", "r") as f:
        data_in = f.read()
    map_raw, commands_raw = data_in.split("\n\n")

    spaces = set()
    walls = set()
    current = None
    facing = 0
    for i, line in enumerate(map_raw.split("\n"), start=1):
        for j, value in enumerate(line, start=1):
            if value == ".":
                spaces.add((j, i))
                if not current:
                    current = (j, i)
            if value == "#":
                walls.add((j, i))
    max_x, max_y = max(spaces, key=lambda x: x[0])[0] + 1, max(spaces, key=lambda x: x[1])[1] + 1
    commands = re.findall(r"\d+|R|L", commands_raw)
    for command in commands:
        if command == "R":
            facing = (facing + 1) % 4
            continue
        if command == "L":
            facing = (facing - 1) % 4
            continue
        for _ in range(int(command)):
            next_candidate = add(current, FACING_MAPPING[facing])
            if next_candidate in walls:
                break
            if next_candidate in spaces:
                current = next_candidate
            else:
                while True:
                    next_candidate = add(next_candidate, FACING_MAPPING[facing])
                    next_candidate = next_candidate[0] % max_x, next_candidate[1] % max_y
                    if next_candidate in walls:
                        break
                    if next_candidate in spaces:
                        current = next_candidate
                        break
    print(1000 * current[1] + 4 * current[0] + facing)
