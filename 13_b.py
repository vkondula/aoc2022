import json
from typing import Optional

from itertools import zip_longest
from functools import cmp_to_key


def int_compare(a, b) -> Optional[bool]:
    if a == b:
        return None
    return a < b

def compare(first, second):
    if isinstance(first, int):
        if isinstance(second, list):
            return compare([first], second)
        return int_compare(first, second)
    if isinstance(first, list):
        if isinstance(second, int):
            return compare(first, [second])
        for a, b in zip_longest(first, second):
            if a is None:
                return True
            if b is None:
                return False
            if (retval := compare(a, b)) is not None:
                return retval
        return None

if __name__ == '__main__':
    with open("inputs/13.txt", "r") as f:
        data_in = f.read()

    groups = []
    retval = []
    for group in data_in.split("\n\n"):
        raw = "[" + group.replace("\n", ",") + "]"
        first, second = json.loads(raw)
        groups += [first, second]
    groups += [[[2]], [[6]]]
    for i, first in enumerate(groups):
        current = 0
        for j, second in enumerate(groups):
            if i == j:
                continue
            if compare(first, second) is False:
                current += 1
        retval.append(current)
    print((retval[-1] + 1) * (retval[-2] + 1))
