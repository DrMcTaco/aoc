from aocd import get_data
from dotenv import load_dotenv

load_dotenv()
data = get_data(day=5, year=2020)


def parse_boarding_pass(bpass: str):
    row = int(bpass[0:7].replace("F", "0").replace("B", "1"), 2)
    col = int(bpass[7:].replace("L", "0").replace("R", "1"), 2)
    id = row * 8 + col
    print(f"row: {row}  col: {col}  id: {id}")
    return row, col, id

ids = [parse_boarding_pass(bpass)[2] for bpass in data.splitlines()]
ids.sort()
full_plane = set(range(min(ids), max(ids)))
my_seat = list(full_plane - set(ids))
print(f"The highest seat ID was: {max(ids)}")
print(f"My seat ID: {my_seat[0]}")

