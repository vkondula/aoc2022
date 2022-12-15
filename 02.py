def unify(value: str) -> int:
    return ord(value) - ord("X" if value > "C" else "A")


def win(value: int, other: int) -> int:
    if value == other:
        return 3
    if (value + 2) % 3 == other:
        return 6
    return 0


if __name__ == '__main__':
    with open("inputs/2.txt", "r") as f:
        data_in = f.read()
    total = 0
    for row in data_in.split("\n"):
        other, value = row.split(" ")
        total += unify(value) + win(unify(value), unify(other)) + 1
    print(total)
