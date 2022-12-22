import re
from collections import defaultdict

SIDE = 50
FACING_MAPPING = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0] * b[0], a[1] * b[1]


def get_index_map(start, existing):
    retval = {start: 0}
    neighbours = defaultdict(dict)
    next_side_index = 1
    while len(retval) != 6:
        for corner, side_index in retval.copy().items():
            for direction_index in range(4):
                new_corner = add(mul(FACING_MAPPING[direction_index], (SIDE, SIDE)), corner)
                if new_corner in existing and new_corner not in retval:
                    retval[new_corner] = next_side_index
                    neighbours[side_index][direction_index] = next_side_index
                    neighbours[next_side_index][(direction_index + 2) % 4] = side_index
                    next_side_index += 1
    while not all(len(a) == 4 for a in neighbours.values()):
        for side in neighbours:
            for i in range(4):
                if i not in neighbours[side]:
                    continue
                neighbour_side = neighbours[side][i]
                if side not in neighbours[neighbour_side].values():
                    # no reverse mapping
                    continue
                rev_i = {value: key for key, value in neighbours[neighbour_side].items()}[side]
                for diff in [-1, 1]:
                    self_direction_index = (i + diff) % 4
                    neighbour_direction_index = (rev_i - diff) % 4
                    if self_direction_index in neighbours[side]:
                        # already have it
                        continue
                    if neighbour_direction_index not in neighbours[neighbour_side]:
                        # neighbour does not have it
                        continue
                    neighbours[side][self_direction_index] = neighbours[neighbour_side][neighbour_direction_index]

    return {value: key for key, value in retval.items()}, neighbours


def get_location_mapping(mapping: dict):
    retval = []
    for key in sorted(mapping.keys()):
        base = mapping[key]
        retval.append({
            (base[0] + i, base[1] + j)
            for i in range(SIDE)
            for j in range(SIDE)
        })
    return retval


def get_side(location, location_mapping):
    for i, values in enumerate(location_mapping):
        if location in values:
            return i
    raise KeyError


def get_offset(location: (int, int), facing: (int, int), location_mapping):
    """Get left offset from pov."""
    side = get_side(location, location_mapping)
    current = location
    counter = 0
    while True:
        current = add(current, FACING_MAPPING[(facing - 1) % 4])
        if current not in location_mapping[side]:
            break
        counter += 1
    return counter


def new_position(side: int, facing: (int, int), offset: int, mapping):
    base_corner = mapping[side]
    diff_corner = {
        0: (0, 0),
        1: (SIDE - 1, 0),
        2: (SIDE - 1, SIDE - 1),
        3: (0, SIDE - 1)
    }[facing]
    corner = add(base_corner, diff_corner)
    facing_right = (facing + 1) % 4
    absolut_offset = FACING_MAPPING[facing_right][0] * offset, FACING_MAPPING[facing_right][1] * offset
    return add(corner, absolut_offset)


def main():
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
    existing = spaces | walls
    mapping, neighbours = get_index_map(current, existing)
    neighbours_reversed = {
        side: {value: key for key, value in record.items()}
        for side, record in neighbours.items()
    }
    location_mapping = get_location_mapping(mapping)
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
                current_side = get_side(current, location_mapping)
                next_side = neighbours[current_side][facing]
                new_facing = (neighbours_reversed[next_side][current_side] + 2) % 4
                offset = get_offset(current, facing, location_mapping)
                next_candidate = new_position(next_side, new_facing, offset, mapping)
                if next_candidate in walls:
                    break
                if next_candidate in spaces:
                    current = next_candidate
                    facing = new_facing
    print(1000 * current[1] + 4 * current[0] + facing)


if __name__ == '__main__':
    main()
