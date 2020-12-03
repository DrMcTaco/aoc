from pathlib import Path

def main(raw_map: str):
    s_x, s_y = (3, 1)
    x, y = (0, 0)
    big_map = raw_map.splitlines()
    width = len(big_map[0])
    trees = 0
    while y < len(big_map):
        if big_map[y][x % width] == "#":
            trees += 1
        x += s_x
        y += s_y

    print(trees)


if __name__ == "__main__":
    raw_map = Path("map.txt").open().read()
    main(raw_map)