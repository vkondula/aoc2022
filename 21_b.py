import re

from sympy import solve, sympify


if __name__ == '__main__':
    with open("inputs/21.txt", "r") as f:
        data_in = f.readlines()
    mapping = {}
    func = None
    for line in data_in:
        if match := re.search("(\w+): (\d+)", line):
            if match.group(1) == "humn":
                continue
            mapping[match.group(1)] = match.group(2)
            continue
        if match := re.search("(\w+): (\w+ [+-/*] \w+)", line):
            if match.group(1) == "root":
                match = re.search("\w+: (\w+) [+-/*] (\w+)", line)
                func = sympify(f"{match.group(1)} - {match.group(2)}")
                continue
            mapping[match.group(1)] = match.group(2)
            continue
        raise KeyError
    changed = True
    while changed:
        changed = False
        for key in func.free_symbols:
            if key.name in mapping:
                func = func.subs({key: f"({mapping[key.name]})"})
                changed = True
    print(solve(func)[0])
