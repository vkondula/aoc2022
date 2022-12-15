def parse(row):
    retval = []
    for group in row.split(","):
        l, h = group.split("-")
        retval.append(set(range(int(l), int(h) + 1)))
    return retval


if __name__ == '__main__':
    with open("inputs/4.txt", "r") as f:
        data_in = f.readlines()
    total = 0
    for row in data_in:
        one, two = parse(row)
        if len(one & two) == min(len(one), len(two)):
            total += 1
    print(total)
