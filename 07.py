import re
import random

from boltons.iterutils import get_path


directory_mapping = {}


def get_value(directory, name):
    value = directory.get("__value") or 0
    for key in directory:
        if key == "__value":
            continue
        value += get_value(directory[key], key)
    directory_mapping[str(random.randint(0, 1000)) + "_" + name] = value
    return value


if __name__ == '__main__':
    with open("inputs/7.txt", "r") as f:
        data_in = f.readlines()
    sum_dir = {}
    path = []
    current_sum = 0
    for command in data_in[1:]:
        if match := re.match("[$] cd (.*)", command):
            current_sum_dir = get_path(sum_dir, path)
            if match.group(1) == "..":
                path = path[:-1]
            else:
                path += [match.group(1)]
                current_sum_dir[match.group(1)] = {}
            current_sum = 0
        if command == "$ ls\n":
            current_sum = 0
        if match := re.match("(\d+) ([^ ]+)", command):
            current_sum_dir = get_path(sum_dir, path)
            current_sum += int(match.group(1))
            current_sum_dir["__value"] = current_sum
    get_value(sum_dir, "/")
    retval = 0
    for key in directory_mapping:
        if directory_mapping[key] <= 100000:
            retval += directory_mapping[key]
    print(retval)
