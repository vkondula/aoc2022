DIRECTION_MAPPING = {
    (0, -1): (range(-1,2), [-1]),
    (0, 1): (range(-1,2), [1]),
    (-1, 0): ([-1], range(-1, 2)),
    (1, 0): ([1], range(-1, 2)),
}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def adjacent(location):
    return {
        (location[0] + i - 1, location[1] + j - 1)
        for i in range(3)
        for j in range(3)
        if i != 1 or j != 1
    }


def adjacent_present(location, direction, elves):
    x_range, y_range = DIRECTION_MAPPING[direction]
    for y in y_range:
        for x in x_range:
            if add(location, (x, y)) in elves:
                return True
    return False


def dump(elves, print_map=False):
    min_x = min(elves.keys(), key=lambda x: x[0])[0]
    max_x = max(elves.keys(), key=lambda x: x[0])[0]
    min_y = min(elves.keys(), key=lambda x: x[1])[1]
    max_y = max(elves.keys(), key=lambda x: x[1])[1]
    print((max_x - min_x + 1) * (max_y - min_y + 1) - len(elves))
    if print_map:
        print("==========")
        for y in range(min_y, max_y + 1):
            line = [
                "#" if (x, y) in elves else "."
                for x in range(min_x, max_x + 1)
            ]
            print("".join(line))


def main():
    with open("inputs/23.txt", "r") as f:
        data_in = f.readlines()
    elves = {}
    for i, line in enumerate(data_in):
        for j, value in enumerate(line):
            if value == "#":
                elves[(j, i)] = None
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    moving = True
    while moving:
        rev_target = {}
        counter += 1
        if counter == 11:
            break
        for elf in elves:
            possible = adjacent(elf)
            if not (possible & elves.keys()):
                continue
            for direction in directions:
                if not adjacent_present(elf, direction, elves):
                    destination = add(direction, elf)
                    if destination in rev_target:
                        second_elf = rev_target[destination]
                        elves[second_elf] = None
                    else:
                        rev_target[destination] = elf
                        elves[elf] = destination
                    break
        tmp = directions.pop(0)
        directions.append(tmp)
        moving = len(set(elves.values())) > 1
        elves = {value if value else key: None for key, value in elves.items()}
    dump(elves)

if __name__ == '__main__':
    main()
