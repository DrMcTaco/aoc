from pathlib import Path

from adventofcode.day1.generic import prod

def count_tree_hits(raw_map: str, slope: tuple):
    s_x, s_y = slope
    x, y = (0, 0)
    big_map = raw_map.splitlines()
    width = len(big_map[0])
    trees = 0
    while y < len(big_map):
        if big_map[y][x % width] == "#":
            trees += 1
        x += s_x
        y += s_y

    print(f"On the slope: {slope} you hit {trees} trees")
    return trees


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

if __name__ == "__main__":
    raw_map = Path("map.txt").open().read()
    print(prod([count_tree_hits(raw_map, slope) for slope in slopes]))