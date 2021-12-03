from typing import List
import re

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()


def parse_contents(rule: str):
    rule = rule.strip()
    if rule == "no other bags.":
        return (0, None)
    match = re.match(r"(?P<num>\d*) (?P<color>.*)", rule.split("bag")[0])

    return int(match.group("num")), match.group("color").strip()


def parse_rule(line, nodes, edges):
    container, contents = line.split(" bags contain ")
    nodes.add(container)
    if edges.get(container):
        edges[container].extend([parse_contents(bag) for bag in contents.split(",")])
    else:
        edges[container] = [parse_contents(bag) for bag in contents.split(",")]


def main(data_: str, target: str):
    nodes = set()
    edges = {}
    can_contain = set()
    [parse_rule(line, nodes, edges) for line in data_.splitlines()]

    def check_can_contain(target: str):
        for color, contents in edges.items():
            if target in [rule[1] for rule in contents]:
                can_contain.add(color)
                check_can_contain(color)

    check_can_contain(target)
    print(f"{len(can_contain)} bags can contain a {target} bag")

    def sum_contents(target: str):
        sum = 1  # this bag
        for count, color in edges[target]:
            if not color:
                return 1
            sum += count * sum_contents(color)
        return sum

    print(f"A {target} bag conatins {sum_contents(target) - 1} bags")


if __name__ == "__main__":
    data = get_data(day=7, year=2020)
    main(data, target="shiny gold")