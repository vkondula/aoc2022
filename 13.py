import json
from typing import Optional

from itertools import zip_longest


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

    counter = 0
    for i, group in enumerate(data_in.split("\n\n"), start=1):
        raw = "[" + group.replace("\n", ",") + "]"
        first, second = json.loads(raw)
        if compare(first, second) is not False:
            counter += i
    print(counter)
