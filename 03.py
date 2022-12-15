def evaluate(value):
    if "A" <= value <= "Z":
        return ord(value) - ord("A") + 27
    return ord(value) - ord("a") + 1


if __name__ == '__main__':
    with open("inputs/3.txt", "r") as f:
        data_in = f.readlines()
    print(
        sum(
            evaluate(list(set(row[:len(row)//2]) & set(row[len(row)//2:]))[0])
            for row in data_in
        )
    )
