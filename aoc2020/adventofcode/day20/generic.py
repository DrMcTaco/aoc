from dataclasses import dataclass
from math import sqrt
from typing import List, Set, Tuple

from aocd import get_data
from dotenv import load_dotenv

from adventofcode.day1.generic import prod

load_dotenv()


def hflip(matrix):
    return [r[::-1] for r in matrix]


def vflip(matrix):
    return matrix[::-1]


def rotate(matrix):
    return [list(r) for r in zip(*matrix[::-1])]


@dataclass
class Tile:
    id: int
    data: List[str]

    def __hash__(self) -> int:
        return self.id

    @classmethod
    def from_string(cls, string):
        id, *data = string.splitlines()
        return cls(int(id.split()[1].strip(":")), data)

    @property
    def image(self: "Tile") -> List[List[str]]:
        return [row[1:-1] for row in self.data[1:-1]]

    @property
    def edges(self):
        return [
            "".join(row[-1] for row in self.data),
            self.data[-1],
            "".join(row[0] for row in self.data),
            self.data[0],
        ]

    @property
    def left(self: "Tile") -> str:
        return self.edges[2]

    @property
    def right(self: "Tile") -> str:
        return self.edges[0]

    @property
    def top(self: "Tile") -> str:
        return self.edges[3]

    @property
    def bottom(self: "Tile") -> str:
        return self.edges[1]

    def rotate(self: "Tile") -> "Tile":
        return Tile(self.id, ["".join(r) for r in zip(*self.data[::-1])])

    def mirror_horizontal(self: "Tile") -> "Tile":
        return Tile(self.id, [r[::-1] for r in self.data])

    def mirror_vertical(self: "Tile") -> "Tile":
        return Tile(self.id, self.data[::-1])


def build_map(
    tiles: List["Tile"],
    grid: List[List["Tile"]],
    seen: Set[int],
    pos: Tuple[int, int] = (0, 0),
):
    x, y = pos
    # base case: completed grid
    if y == len(grid):
        return grid

    for tile in tiles:
        if tile.id in seen:
            continue

        if x > 0 and grid[y][x - 1].right != tile.left:
            continue
        if y > 0 and grid[y - 1][x].bottom != tile.top:
            continue

        grid[y][x] = tile
        nex_pos = (x + 1, y) if x < len(grid[0]) - 1 else (0, y + 1)
        result = build_map(tiles, grid, seen | {tile.id}, nex_pos)
        if result is not None:
            grid = result
            break
        grid[y][x] = None
    else:
        # executed iff the loop exits without a break
        grid = None

    return grid


def generate_grid(tiles: List["Tile"], size: int):
    candidates = []
    for tile in tiles:
        for _ in range(2):
            candidates.append(tile)
            candidates.append(tile.mirror_horizontal())
            candidates.append(tile.mirror_vertical())
            candidates.append(candidates[-1].mirror_horizontal())
            tile = tile.rotate()
    return build_map(
        candidates, [[None for _ in range(size)] for _ in range(size)], set()
    )


def full_image(grid: List[List["Tile"]]):
    pixels = []
    for row in grid:
        pixel_row = [[] for _ in range(len(row[0].left) - 2)]
        for tile in row:
            for i, image_row in enumerate(tile.image):
                pixel_row[i] += [c for c in image_row]
        pixels += pixel_row
    return pixels


def find_monster(grid, monster):
    image = full_image(grid)
    for _ in range(2):
        if mark_monster(image, monster):
            break

        image = hflip(image)
        if mark_monster(image, monster):
            break

        image = vflip(image)
        if mark_monster(image, monster):
            break

        image = hflip(image)
        if mark_monster(image, monster):
            break

        image = rotate(vflip(image))
    return image


def monster_map(monster):
    map = []
    m_y = len(monster.splitlines())
    for y, line in enumerate(monster.splitlines(), 0):
        m_x = len(line)
        for x, char in enumerate(line, 0):
            if char == "#":
                map += [(y, x)]
    return map, m_y, m_x


def mark_monster(image, monster):
    m_map, m_y, m_x = monster_map(monster)

    x, y = 0, 0
    monsters = 0

    rows = len(image)
    cols = len(image[0])

    while y < rows - m_y:
        while x < cols - m_x:
            if all([image[y + j][x + i] == "#" for j, i in m_map]):
                monsters += 1
                for j, i in m_map:
                    image[y+j][x+i] = "O"
                x += 20
            else:
                x += 1
        x, y = 0, y + 1

    return monsters

def print_image(image):
    for row in image:
        print("".join(row))


monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

if __name__ == "__main__":
    tiles = get_data(day=20, year=2020).split("\n\n")
    tiles = [Tile.from_string(tile) for tile in tiles]
    size = int(sqrt(len(tiles)))
    grid = generate_grid(tiles, size)
    print(grid[0][0].id * grid[0][-1].id * grid[-1][0].id * grid[-1][-1].id)
    image = find_monster(grid, monster)
    print_image(image)
    print(sum(row.count("#") for row in image))
