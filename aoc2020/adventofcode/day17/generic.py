from copy import copy
from dataclasses import dataclass
from itertools import product
from typing import Callable

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


@dataclass
class State:
    grid: set

    def copy(self):
        return State(copy(self.grid))

    def get_neighbors(self, elem: tuple, dim: int = 3):
        if dim == 4:
            w_vals = [elem[0] + n for n in (-1, 0, 1)]
            z_vals = [elem[1] + n for n in (-1, 0, 1)]
            y_vals = [elem[2] + n for n in (-1, 0, 1)]
            x_vals = [elem[3] + n for n in (-1, 0, 1)]
            return [
                (w, z, y, x)
                for w, z, y, x in product(w_vals, z_vals, y_vals, x_vals)
                if (w, z, y, x) != elem
            ]

        z_vals = [elem[0] + n for n in (-1, 0, 1)]
        y_vals = [elem[1] + n for n in (-1, 0, 1)]
        x_vals = [elem[2] + n for n in (-1, 0, 1)]
        return [
            (z, y, x)
            for z, y, x in product(z_vals, y_vals, x_vals)
            if (z, y, x) != elem
        ]

    def apply_rules(self, dim: int = 3):
        self.grid = apply_rules(self.grid, self.get_neighbors, dim=dim)
        return self


def apply_rules(grid: set, get_neighbors: Callable, dim: int = 3):
    active_counts = {}
    for elem in grid:
        if elem not in active_counts:
            active_counts[elem] = 0
        neighbors = get_neighbors(elem, dim=dim)
        for pos in neighbors:
            if pos not in active_counts:
                active_counts[pos] = 1
            else:
                active_counts[pos] += 1
    for pos, count in active_counts.items():
        if count < 2 or count > 3:
            grid.discard(pos)
        if count == 3:
            grid.add(pos)
    return grid


def run_cycles(cycles: int, init: str, dim: int = 3):
    init_state = set()
    for y, row in enumerate(init.splitlines(), 0):
        for x, val in enumerate(row, 0):
            if val == "#":
                if dim == 4:
                    init_state.add((0, 0, y, x))
                else:
                    init_state.add((0, y, x))
    state = State(init_state)
    history = []
    for i in range(cycles):
        previous_state = state.copy()
        history.append(previous_state.grid)
        state = state.apply_rules(dim=dim)
    history.append(state.grid)
    print(len(state.grid))


if __name__ == "__main__":
    input = get_data(day=17, year=2020)
    run_cycles(6, input)
    run_cycles(6, input, dim=4)