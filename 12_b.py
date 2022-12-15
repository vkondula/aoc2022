from __future__ import annotations

from typing import Optional

import attr


@attr.s(auto_attribs=True)
class Node:
    x: int
    y: int
    height: int
    cost: int
    neighbors: list[Node]

    def build(self):
        for diff_x, diff_y in [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]:
            x, y = self.x + diff_x, self.y + diff_y
            if x == -1 or y == -1 or x == x_max or y == y_max:
                continue
            neighbour = input_parsed[y][x]
            if self.height > neighbour.height + 1:
                continue
            self.neighbors.append(neighbour)


if __name__ == '__main__':
    with open("inputs/12.txt", "r") as f:
        data_in = f.readlines()
    max_value = sum(len(row) for row in data_in)
    input_parsed = [
        [
            Node(i, j, ord(a) - ord('a'), max_value * max_value, [])
            for i, a in enumerate(row) if a != "\n"
        ]
        for j, row in enumerate(data_in)
    ]
    x_max = len(input_parsed[0])
    y_max = len(input_parsed)
    start, end = None, None
    for row in input_parsed:
        for node in row:
            if node.height + ord("a") == ord("S"):
                start = node
                node.height = 0
            if node.height + ord("a") == ord("E"):
                end = node
                end.cost = 0
                node.height = ord("z") - ord("a")
    for row in input_parsed:
        for node in row:
            node.build()
    stack = [end]
    while stack:
        current = stack.pop()
        for neighbour in current.neighbors:
            if neighbour.cost > current.cost + 1:
                neighbour.cost = current.cost + 1
                stack.append(neighbour)
    potential_starts = []
    for row in input_parsed:
        for node in row:
            if node.height == 0:
                potential_starts.append(node.cost)
    print(min(potential_starts))
    # for row in input_parsed:
    #     print("".join([f"-{node.cost + 10}-" for node in row]))

