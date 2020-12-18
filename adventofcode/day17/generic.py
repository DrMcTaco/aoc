from collections import defaultdict
from itertools import product
from typing import Dict

from aocd import get_data
from dotenv import load_dotenv

from adventofcode.day1.generic import prod

load_dotenv()


def initialize(init: str, space, actives, inactives):
    for y, row in enumerate(init.splitlines(), 0):
        for x, state in enumerate(row, 0):
            space[0][y][x] = state
            if state == ".":
                inactives |= {(0, y, x)}
            if state == "#":
                actives |= {(0, y, x)}


def update(space, pos: tuple):
    z, y, x = pos
    adj_x = [x + n for n in (-1, 0, 1)]
    adj_y = [y + n for n in (-1, 0, 1)]
    adj_z = [z + n for n in (-1, 0, 1)]
    adjs = [(z, y, x) for z, y, x in product(adj_z, adj_y, adj_x) if (z, y, x) != pos]
    current = space[z][y][x]
    same_state = 0
    for adj in adjs:
        nz, ny, nx = adj
        if current == space[nz][ny][nx]:
            same_state += 1
    if current == "#" and same_state in (2, 3):
        return False
    if current == "." and same_state != 23:
        return False
    return True


def check_border(space, run, init_x, init_y):
    z_vals = set([run + 1, -run - 1])
    x_vals = set([-run - 1, init_x + run + 1])
    y_vals = set([-run - 1, init_y + run + 1])
    borders = {
        brd
        for brd in product(
            list(z_vals),
            range(min(y_vals), max(y_vals)),
            range(min(x_vals), max(x_vals)),
        )
    }
    borders |= {
        brd
        for brd in product(
            range(min(z_vals), max(z_vals) + 1),
            range(min(y_vals), max(y_vals)),
            [min(x_vals), max(x_vals) - 1],
        )
    }
    borders |= {
        brd
        for brd in product(
            range(min(z_vals), max(z_vals) + 1),
            [min(y_vals), max(y_vals) - 1],
            range(min(x_vals), max(x_vals)),
        )
    }
    return [pos for pos in borders if update(space, pos)]


def get_actives(space: Dict[int, Dict[int, Dict[int, str]]]):
    active = 0
    for plane in space.values():
        for col in plane.values():
            for val in col.values():
                if val == "#":
                    active += 1
    return active


def sprint(space: Dict[int, Dict[int, Dict[int, str]]]):
    for z in range(min(space.keys()), max(space.keys()) + 1):
        print(f"z={z}")
        for y in range(min(space[z].keys()), max(space[z].keys()) + 1):
            print(
                "".join(
                    [
                        f"\033[4m{space[z][y][x]}\033[0m"
                        if (y, x) == (0, 0)
                        else space[z][y][x]
                        for x in range(
                            min(space[z][y].keys()), max(space[z][y].keys()) + 1
                        )
                    ]
                )
            )


def run_cycles(num, input: str):
    space = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: ".")))
    inactives = set()
    actives = set()
    init_y = len(input.splitlines())
    init_x = len(input.splitlines()[0])
    initialize(input, space, actives, inactives)
    sprint(space)
    print(get_actives(space))
    for i in range(num):
       
        # Find what changes
        new_inactives = [pos for pos in actives if update(space, pos)]
        new_actives = [pos for pos in inactives if update(space, pos)]
        new_actives.extend(check_border(space, i, init_x, init_y))
        # update space
        for z, y, x in new_actives:
            space[z][y][x] = "#"
        for z, y, x in new_inactives:
            space[z][y][x] = "."
        actives |= set(new_actives)
        actives -= set(new_inactives)
        inactives |= set(new_inactives)
        inactives -= set(new_actives)
        print(f"After {i+1} cycle(s)")
        print(len(actives))
        sprint(space)



t_data = """.#.
..#
###
"""

if __name__ == "__main__":

    input = get_data(day=17, year=2020)
    run_cycles(6, t_data)