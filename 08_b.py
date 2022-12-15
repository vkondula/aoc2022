def scenic_score(forest, i, j, max_index):
    retval = 1
    for inc_i, inc_j in [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]:
        tmp_i, tmp_j = i, j
        counter = 1
        while all(value != limit for value in [tmp_i, tmp_j] for limit in [0, max_index]):
            tmp_i += inc_i
            tmp_j += inc_j
            if forest[tmp_i][tmp_j] >= forest[i][j]:
                break
            counter += 1
        else:
            counter -= 1
        retval *= counter
    return retval


if __name__ == '__main__':
    with open("inputs/8.txt", "r") as f:
        data_in = f.readlines()
    parsed = [
        [int(value) for value in row if value != "\n"]
        for row in data_in
    ]
    dim_i, dim_j = len(parsed), len(parsed[0])
    print(max(
        scenic_score(parsed, i, j, dim_j - 1)
        for j in range(1, dim_j-1)
        for i in range(1, dim_i-1)
    ))


