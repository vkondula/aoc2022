if __name__ == '__main__':
    with open("inputs/8.txt", "r") as f:
        data_in = f.readlines()
    parsed = [
        [int(value) for value in row if value != "\n"]
        for row in data_in
    ]
    dim_i, dim_j = len(parsed), len(parsed[0])
    visible = set()
    for range_outer, range_inner, reversed in [
        (range(dim_i), range(dim_j), False),
        (range(dim_i), range(dim_j-1, -1, -1), False),
        (range(dim_j), range(dim_i), True),
        (range(dim_j), range(dim_i-1, -1, -1), True),
    ]:
        for i in range_outer:
            last = -1
            for j in range_inner:
                tree = parsed[i][j] if not reversed else parsed[j][i]
                if tree > last:
                    last = tree
                    visible.add(f"{i}-{j}" if not reversed else f"{j}-{i}")
    print(len(visible))

