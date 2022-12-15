if __name__ == '__main__':
    with open("inputs/1.txt", "r") as f:
        data_in = f.read()
    print(
        sum(
            sorted(
                (
                    sum(int(value) for value in  group.split("\n"))
                    for group in data_in.split("\n\n")
                ),
                reverse=True
            )[0:3]
        )
    )
