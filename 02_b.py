def unify(value: str) -> int:
    return ord(value) - ord("X" if value > "C" else "A")


def win(value: int, other: int) -> int:
    if value == other:
        return 3
    if (value + 2) % 3 == other:
        return 6
    return 0


def resolve(other:int, result: int) -> int:
    return (other + result - 1) % 3


if __name__ == '__main__':
    with open("inputs/2.txt", "r") as f:
        data_in = f.read()
    total = 0
    for row in data_in.split("\n"):
        other, value = row.split(" ")
        total += unify(value) * 3 + resolve(unify(other), unify(value)) + 1
    print(total)
