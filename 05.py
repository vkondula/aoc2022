import re

import more_itertools


def parse_command(row):
    match = re.search(r"move (\d+) from (\d+) to (\d+)", row)
    return [int(match.group(index)) for index in range(1, 4)]


def parse_stack(stack_raw):
    blocks = [
        [
            row[index:min(index + 4, len(row))] for index in range(0, len(row), 4)
        ]
        for row in stack_raw.split("\n")
    ]
    transposed = [list(record) for record in more_itertools.unzip(blocks)]
    return [
        [
            item.strip("[] ")
            for item in row
            if "A" <= item.strip("[] ") <= "Z"
        ][::-1]
        for row in transposed
    ]


def perform_commands(stacks, commands):
    for count, from_, to_ in commands:
        for _ in range(count):
            tmp = stacks[from_ - 1].pop()
            stacks[to_ - 1] += [tmp]
    return stacks


if __name__ == '__main__':
    with open("inputs/5.txt", "r") as f:
        data_in = f.read()
    stack_raw, commands_raw = data_in.split("\n\n")
    commands = [parse_command(row) for row in commands_raw.split("\n") if row]
    stack = parse_stack(stack_raw)
    new_stack = perform_commands(stack, commands)
    print("".join([stack[-1] for stack in new_stack]))
