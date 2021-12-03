from copy import deepcopy
from itertools import product
from typing import List

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def update(x: int, y: int, layout: List[str]):
    curr = layout[y][x]
    pos_y = [n + y for n in (-1, 0, 1) if 0 <= n + y < len(layout)]
    pos_x = [n + x for n in (-1, 0, 1) if 0 <= n + x < len(layout[0])]
    adjs = [(adj[0], adj[1]) for adj in product(pos_y, pos_x) if adj != (y, x)]

    if curr == "L":
        if all([layout[ny][nx] != "#" for ny, nx in adjs]):
            return "#"
    elif curr == "#":
        if [layout[ny][nx] == "#" for ny, nx in adjs].count(True) >= 4:
            return "L"
    return curr


def update2(x: int, y: int, layout: List[str]):
    adjs = []
    curr = layout[y][x]
    for yd in (-1, 0, 1):
        for xd in (-1, 0, 1):
            if yd == 0 and xd == 0:
                continue
            n = 1
            while True:
                if not (
                    0 <= y + yd * n < len(layout) and 0 <= x + xd * n < len(layout[0])
                ):
                    break
                if y + yd * n >= len(layout) or x + xd * n >= len(layout[0]):
                    break
                if layout[y + yd * n][x + xd * n] != ".":
                    adjs.append((y + yd * n, x + xd * n))
                    break
                n += 1
    if curr == "L":
        if all([layout[ny][nx] != "#" for ny, nx in adjs]):
            return "#"
    elif curr == "#":
        if [layout[ny][nx] == "#" for ny, nx in adjs].count(True) >= 5:
            return "L"
    return curr


def get_occupied(layout, method):
    current = deepcopy(layout)
    next = [["" for _ in range(len(layout[0]))] for _ in range(len(layout))]
    while True:
        for y, row in enumerate(current, 0):
            for x, seat in enumerate(row, 0):
                if seat == ".":
                    next[y][x] = "."
                else:
                    if method == 1:
                        next[y][x] = update(x, y, current)
                    else:
                        next[y][x] = update2(x, y, current)
        if current == next:
            break
        current = deepcopy(next)

    occupied = sum([row.count("#") for row in current])

    print(occupied)


if __name__ == "__main__":
    data = get_data(day=11, year=2020)
    get_occupied(data.splitlines(), 1)
    get_occupied(data.splitlines(), 2)