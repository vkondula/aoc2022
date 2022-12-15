import re
from typing import Callable
from operator import add, mul

import attr


@attr.s(auto_attribs=True)
class Item:
    values: dict[int, int]

    @classmethod
    def build(cls, divisibles, value):
        return cls({
            divisible: value % divisible
            for divisible in divisibles
        })

    def perform(self, operation: Callable, value):
        for key in self.values:
            self.values[key] = operation(self.values[key], value) % key

    def exp(self):
        for key in self.values:
            self.values[key] =  (self.values[key] *  self.values[key]) % key

    def is_divisible(self, value):
        return self.values[value] == 0

    def get(self, key):
        return self.values[key]


@attr.s(auto_attribs=True)
class Monkey:
    items: list[Item]
    operator: Callable
    operand: int
    divisible_by: int
    next_monkey: tuple[int, int]
    inspected: int

    @classmethod
    def build(cls, text, divisibles):
        return cls(
            [Item.build(divisibles, int(a)) for a in re.search(r"Starting items: ([^\n]*)\n", text).group(1).split(", ")],
            add if "+" in text else mul,
            int(re.search(r"[+*] (\d+)", text).group(1)) if re.search(r"[+*] (\d+)", text) else 0,
            int(re.search(r"divisible by (\d+)", text).group(1)),
            (
                int(re.search(r"If false: throw to monkey (\d+)", text).group(1)),
                int(re.search(r"If true: throw to monkey (\d+)", text).group(1)),
            ),
            0,
        )

    def perform_round(self):
        for item in self.items:
            self.inspected += 1
            if self.operand:
                item.perform(self.operator, self.operand)
            else:
                item.exp()
            monkeys[self.next_monkey[item.is_divisible(self.divisible_by)]].items += [item]
        self.items = []


if __name__ == '__main__':
    with open("inputs/11.txt", "r") as f:
        data_in = f.read()
    monkeys_raw = data_in.split("\n\n")
    divs = [int(a) for a in re.findall(r"divisible by (\d+)", data_in)]
    monkeys = [Monkey.build(text, divs) for text in monkeys_raw]
    for _ in range(10000):
        for monkey in monkeys:
            monkey.perform_round()
    print(sorted(monkeys, key=lambda x: x.inspected)[-1].inspected * sorted(monkeys, key=lambda x: x.inspected)[-2].inspected)
