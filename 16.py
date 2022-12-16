import re
from typing import NamedTuple
from collections import defaultdict


class Location(NamedTuple):
    name: str
    flow: int
    leads: list[str]


class Snapshot(NamedTuple):
    time: int
    location: str
    opened: list[str]
    flown: int = 0


if __name__ == '__main__':
    with open("inputs/16.txt", "r") as f:
        data_in = f.readlines()
    guide = {}
    for row in data_in:
        match = re.search(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([^\n]*)", row)
        guide[match.group(1)] = Location(match.group(1), int(match.group(2)), match.group(3).split(", "))
    flow_mapping = {location.name: location.flow for location in guide.values() if location.flow}
    all_mapping = {}
    for start_location in flow_mapping.keys() | {"AA"}:
        all_mapping[start_location] = defaultdict(lambda: 31, {start_location: 0})
        current_mapping = all_mapping[start_location]
        stack = [guide[start_location]]
        while stack:
            current = stack.pop()
            for neighbour_name in current.leads:
                neighbour = guide[neighbour_name]
                if current_mapping[neighbour_name] > current_mapping[current.name] + 1:
                    current_mapping[neighbour_name] = current_mapping[current.name] + 1
                    stack.append(neighbour)

    stack = [Snapshot(0, "AA", [])]
    final_max = 0
    while stack:
        snapshot = stack.pop()
        for location, flow in flow_mapping.items():
            final_max = max(final_max, snapshot.flown)
            if location in snapshot.opened:
                continue
            travel_time = all_mapping[snapshot.location][location]
            if snapshot.time + travel_time > 30:
                continue
            stack.append(
                Snapshot(
                    snapshot.time + travel_time + 1,
                    location,
                    snapshot.opened + [location],
                    snapshot.flown + (30 - travel_time - 1 - snapshot.time) * flow_mapping[location]
                )
            )
    print(final_max)
