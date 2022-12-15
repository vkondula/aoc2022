import re

if __name__ == '__main__':
    with open("inputs/10.txt", "r") as f:
        data_in = f.readlines()
    values = []
    value = 1
    i = 0
    for line in data_in:
        i += 1
        values.append(value)
        if find := re.search("addx (-?\d+)", line):
            i += 1
            values.append(value)
            value += int(find.group(1))

    line = ""
    for i, value in enumerate(values):
        current = i % 40
        if abs(value - current) < 2:
            line += "#"
        else:
            line += "."
        if current == 39:
            print(line)
            line = ""

