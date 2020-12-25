from collections import defaultdict
from copy import copy
from datetime import date
from dataclasses import dataclass
from typing import DefaultDict, List, Callable

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()


t = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""


@dataclass
class State:
    grid: set

    def copy(self):
        return State(copy(self.grid))

    def get_neighbors(self, elem: tuple):
        w = [n + m for n, m in zip(elem, (-1, 1, 0))]
        sw = [n + m for n, m in zip(elem, (-1, 0, 1))]
        se = [n + m for n, m in zip(elem, (0, -1, 1))]
        e = [n + m for n, m in zip(elem, (1, -1, 0))]
        ne = [n + m for n, m in zip(elem, (1, 0, -1))]
        nw = [n + m for n, m in zip(elem, (0, 1, -1))]
        return [tuple(w), tuple(sw), tuple(se), tuple(e), tuple(ne), tuple(nw)]

    def apply_rules(self):
        self.grid = apply_rules(self.grid, self.get_neighbors)
        return self


def apply_rules(grid: set, get_neighbors: Callable):
    active_counts = {}
    for elem in grid:
        if elem not in active_counts:
            active_counts[elem] = 0
        neighbors = get_neighbors(elem)
        for pos in neighbors:
            if pos not in active_counts:
                active_counts[pos] = 1
            else:
                active_counts[pos] += 1
    for pos, count in active_counts.items():
        if count == 0 or count > 2:
            grid.discard(pos)
        if count == 2:
            grid.add(pos)
    return grid


def run_cycles(cycles: int, init: DefaultDict[tuple, str]):
    init_state = set()
    for pos in [pos for pos, color in init.items() if color == "b"]:
        init_state.add(pos)
    state = State(init_state)
    history = []
    for i in range(cycles):
        previous_state = state.copy()
        history.append(previous_state.grid)
        state = state.apply_rules()
    history.append(state.grid)
    print(len(state.grid))


def install_floor(instructions: List[str]):
    tiles = defaultdict(lambda: "w")
    for instruction in instructions:
        instruction = list(instruction)
        x, y, z = 0, 0, 0
        while instruction:
            if "".join(instruction[0:2]) in ["se", "sw", "ne", "nw"]:
                move = str(instruction.pop(0))
                move += str(instruction.pop(0))
            else:
                move = str(instruction.pop(0))

            if move == "se":
                y -= 1
                z += 1
            elif move == "nw":
                y += 1
                z -= 1
            elif move == "e":
                x += 1
                y -= 1
            elif move == "w":
                x -= 1
                y += 1
            elif move == "ne":
                x += 1
                z -= 1
            elif move == "sw":
                x -= 1
                z += 1
        if tiles[(x, y, z)] == "b":
            tiles[(x, y, z)] = "w"
        else:
            tiles[(x, y, z)] = "b"
    print(sum([1 for val in tiles.values() if val == "b"]))
    return tiles


if __name__ == "__main__":
    moves = get_data(day=24, year=2020).splitlines()
    # moves = t.splitlines()
    tiles = install_floor(moves)
    run_cycles(100, tiles)
