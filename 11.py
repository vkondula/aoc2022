import re
from typing import Callable
from operator import add, mul

import attr


@attr.s(auto_attribs=True)
class Monkey:
    items: list[int]
    operator: Callable
    operand: int
    divisible_by: int
    next_monkey: tuple[int, int]
    inspected: int

    @classmethod
    def build(cls, text):
        return cls(
            [int(a) for a in re.search(r"Starting items: ([^\n]*)\n", text).group(1).split(", ")],
            add if "+" in text else mul,
            int(re.search(r"[+*] (\d+)", text).group(1)) if re.search(r"[+*] (\d+)", text) else 0,
            int(re.search(r"divisible by (\d+)", text).group(1)),
            (
                int(re.search(r"If false: throw to monkey (\d+)", text).group(1)),
                int(re.search(r"If true: throw to monkey (\d+)", text).group(1)),
            ),
            0
        )

    def perform_round(self):
        for item in self.items:
            self.inspected += 1
            second_arg = self.operand or item
            item = self.operator(item, second_arg)
            item //= 3
            monkeys[self.next_monkey[not(item % self.divisible_by)]].items += [item]
        self.items = []



if __name__ == '__main__':
    with open("inputs/11.txt", "r") as f:
        data_in = f.read()
    monkeys_raw = data_in.split("\n\n")
    monkeys = [Monkey.build(text) for text in monkeys_raw]
    for _ in range(20):
        for monkey in monkeys:
            monkey.perform_round()
    print(sorted(monkeys, key=lambda x: x.inspected)[-1].inspected * sorted(monkeys, key=lambda x: x.inspected)[-2].inspected)
