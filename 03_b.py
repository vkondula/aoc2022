from more_itertools import chunked


def evaluate(value):
    if "A" <= value <= "Z":
        return ord(value) - ord("A") + 27
    return ord(value) - ord("a") + 1


if __name__ == '__main__':
    with open("inputs/3.txt", "r") as f:
        data_in = f.readlines()
    print(
        sum(
            evaluate(list(set(row[0][:-1]) & set(row[1][:-1]) & set(row[2][:-1]))[0])
            for row in chunked(data_in, 3)
        )
    )
