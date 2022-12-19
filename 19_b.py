import re
from collections import defaultdict
from typing import NamedTuple, Optional
from math import ceil
from functools import reduce


REPORT = defaultdict(int)
POTENTIAL_GAIN = [(t - 1) * t // 2 for t in range(32, -1, -1)]


class Blueprint(NamedTuple):
    id: int
    ore_ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int

    def cost(self, name, mult = 1):
        if name == "ore":
            return {"ore": mult * self.ore_ore}
        if name == "clay":
            return {"ore": mult * self.clay_ore}
        if name == "obsidian":
            return {"ore": mult * self.obsidian_ore, "clay": mult * self.obsidian_clay}
        if name == "geode":
            return {"ore": mult * self.geode_ore, "obsidian": mult * self.geode_obsidian}
        raise KeyError


def add(a: dict, b: dict):
    return defaultdict(int, {key: a.get(key, 0) + b.get(key, 0) for key in a.keys() | b.keys()})


def turns_until(target: dict, resources: dict, production: dict):
    snap = target.copy()
    for key in snap:
        snap[key] -= resources.get(key, 0)
        if not production.get(key):
            return 1000
    if all(value <= 0 for value in snap.values()):
        return 0
    return max(ceil(snap[key] / production[key]) for key, value in target.items() if value > 0)


class GameSnapshot:
    def __init__(self, blueprint: Blueprint, robots: Optional[defaultdict] = None, resources: Optional[defaultdict] = None, turn: int = 0):
        self.blueprint = blueprint
        self.robots = robots or defaultdict(int, {"ore": 1})
        self.resources = resources or defaultdict(int)
        self.turn = turn

    def excess(self, name):
        if name == "ore":
            return self.robots["ore"] >= max(self.blueprint.cost(name).get("ore") for name in ["ore", "clay", "obsidian", "geode"])
        if name == "clay":
            return self.robots["clay"] >= self.blueprint.obsidian_clay
        if name == "obsidian":
            return self.robots["obsidian"] >= self.blueprint.geode_obsidian
        if name == "geode":
            return False
        raise KeyError

    def next_actions(self):
        REPORT[blueprint.id] = max(REPORT[blueprint.id], self.resources["geode"])
        if self.resources["geode"] * (32 - self.turn) + POTENTIAL_GAIN[self.turn] <= REPORT[blueprint.id]:
            REPORT[blueprint.id] = max(REPORT[blueprint.id], self.resources["geode"] + (32 - self.turn) * self.robots.get("geode", 0))
            return []
        possible = list(filter(lambda x: x[1] < 1000, ((name, self.turns_until(name)) for name in ["ore", "clay", "obsidian", "geode"])))
        if self.turn >= 32:
            return []
        retval = [
           self.copy({name: 1}, self.blueprint.cost(name, -1))
           for name, turns in possible
           if turns == 0 and not self.excess(name)
        ] + [
            self.copy({name: 1}, self.blueprint.cost(name, -1), turns + 1)
            for name, turns in possible
            if self.turn + turns < 32 and turns > 0 and not self.excess(name)
        ]
        if not retval:
            return [self.copy({}, {})]
        return retval

    def turns_until(self, name):
        return turns_until(self.blueprint.cost(name), self.resources, self.robots)

    def copy(self, robots, paid, turn_diff=None):
        turn_diff = (turn_diff or 1)
        produced = defaultdict(int, {key: value * turn_diff for key, value in self.robots.items()})
        resources = add(add(self.resources, produced), paid)
        robots = add(robots, self.robots)
        return self.__class__(
            self.blueprint,
            robots,
            resources,
            self.turn + turn_diff,
        )


if __name__ == '__main__':
    with open("inputs/19.txt", "r") as f:
        data_in = f.readlines()
    parsed = [
        Blueprint(*map(int, re.search(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line).groups()))
        for line in data_in
    ]
    for i, blueprint in enumerate(parsed):
        if i >= 3:
            break
        expand = [GameSnapshot(blueprint)]
        while expand:
            snapshot = expand.pop()
            expand += snapshot.next_actions()
    # print(REPORT)
    print(reduce(lambda x, y: x * y, (value for value in REPORT.values())))
