from math import ceil, sqrt

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()


t = """5764801
# 17807724
"""


def transform(subject, loop_size):
    res = 1
    for _ in range(loop_size):
        res *= subject
        res %= 20201227
    return res


def find_loop(pub):
    """
    solve for x in h = g^x mod p using big step little step
    """
    p = 20201227
    g = 7
    N = ceil(sqrt(p - 1))

    table = {pow(g, i, p): i for i in range(N)}

    c = pow(g, N * (p - 2), p)

    for j in range(N):
        y = (pub * pow(c, j, p)) % p
        if y in table:
            return j * N + table[y]
    return None


if __name__ == "__main__":
    card, door = map(int, get_data(day=25, year=2020).splitlines())
    # card, door = map(int, t.splitlines())
    print(card, door)
    card_loop_size = find_loop(card)
    door_loop_size = find_loop(door)
    key = transform(card, door_loop_size)
    print(key)
    key = transform(door, card_loop_size)
    print(key)