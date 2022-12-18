def get_sides(x, y, z):
    diffs = []
    for i in range(3):
        for value in range(2):
            base = [0.5, 0.5, 0.5]
            base[i] = value
            diffs.append(base)
    return {(int(x) - i, int(y) - j, int(z) - k) for i, j, k in diffs}


def get_max_cube(cubes):
    return tuple(
        max(cubes, key=lambda x: x[i])[i] + 2
        for i in range(3)
    )


def connected(cube, max_cube):
    retval = set()
    for i in range(3):
        for value in [1,-1]:
            tmp = list(cube)
            tmp[i] += value
            for j in range(3):
                if tmp[j] > max_cube[j] or tmp[j] < -1:
                    break
            else:
                retval.add(tuple(tmp))
    return retval


if __name__ == '__main__':
    with open("inputs/18.txt", "r") as f:
        data_in = f.readlines()
    original_cubes = {
        tuple(map(int, line.strip("\n").split(",")))
        for line in data_in
    }
    max_cube = get_max_cube(original_cubes)
    changed = {max_cube}
    water_cubes = set()
    while changed:
        water_cubes |= changed
        changed = set()
        for cube in water_cubes:
            neighbours = connected(cube, max_cube)
            changed |= neighbours - water_cubes - original_cubes
    all_cubes = {
        (i, j, k)
        for i in range(0, max_cube[0])
        for j in range(0, max_cube[1])
        for k in range(0, max_cube[2])
    }
    not_touching_water_cubes = all_cubes - water_cubes
    cubes = [
        get_sides(*cube)
        for cube in not_touching_water_cubes
    ]
    retval = set()
    for i in range(len(cubes)):
        tmp = cubes[i].copy()
        for j in range(len(cubes)):
            if i == j:
                continue
            tmp -= cubes[j]
        retval |= tmp
    print(len(retval))
