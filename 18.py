def get_sides(x, y, z):
    diffs = []
    for i in range(3):
        for value in range(2):
            base = [0.5, 0.5, 0.5]
            base[i] = value
            diffs.append(base)
    return {(int(x) - i, int(y) - j, int(z) - k) for i, j, k in diffs}


if __name__ == '__main__':
    with open("inputs/18.txt", "r") as f:
        data_in = f.readlines()
    cubes = [
        get_sides(*line.strip("\n").split(","))
        for line in data_in
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
