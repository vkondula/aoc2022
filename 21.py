import re
from operator import mul, add, sub, floordiv

OPERATORS = {"+": add, "*": mul, "-": sub, "/": floordiv}

if __name__ == '__main__':
    with open("inputs/21.txt", "r") as f:
        data_in = f.readlines()
    values: dict[str, int] = {}
    pending: dict[str, tuple[str, str, str]] = {}
    for line in data_in:
        if match := re.search("(\w+): (\d+)", line):
            values[match.group(1)] = int(match.group(2))
            continue
        if match := re.search("(\w+): (\w+) ([+-/*]) (\w+)", line):
            pending[match.group(1)] = (match.group(3), match.group(2), match.group(4))
            continue
        raise KeyError
    while pending:
        keys = set(pending.keys())
        for key in keys:
            op, left, right = pending[key]
            if left in values and right in values:
                values[key] = OPERATORS[op](values[left], values[right])
                pending.pop(key)
    print(values["root"])
