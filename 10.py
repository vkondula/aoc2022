import re

if __name__ == '__main__':
    with open("inputs/10.txt", "r") as f:
        data_in = f.readlines()
    signals = [-1]
    value = 1
    i = 0
    for line in data_in:
        i += 1
        signals.append(value * i)
        if find := re.search("addx (-?\d+)", line):
            i += 1
            signals.append(value * i)
            value += int(find.group(1))

    print(sum(value for i, value in enumerate(signals) if i in [20, 60, 100, 140, 180, 220]))
