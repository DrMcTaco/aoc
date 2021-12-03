from aocd import get_data
from dotenv import load_dotenv


load_dotenv()


def move_cups(current, next_cups, num_cups):
    removed = []
    removed.append(next_cups[current])
    for _ in range(2):
        removed.append(next_cups[removed[-1]])

    next_cups[current] = next_cups[removed[-1]]

    target = current - 1
    while target in removed or target == 0:
        target -= 1
        if target < 1:
            target = num_cups
    next_cups[removed[-1]] = next_cups[target]
    next_cups[target] = removed[0]

    return next_cups[current]


def play_game(cups, moves, num_cups=None):
    cups = [int(num) for num in cups]
    if not num_cups:
        num_cups = len(cups)
    next_cup = [-1] * (num_cups + 1)

    for i in range(len(cups) - 1):
        next_cup[cups[i]] = cups[i + 1]
    next_cup[cups[-1]] = max(cups) + 1

    for i in range(max(cups) + 1, num_cups):
        next_cup[i] = i + 1
    next_cup[num_cups] = cups[0]

    current = cups[0]
    for i in range(moves):
        current = move_cups(current, next_cup, num_cups)
    return next_cup


t = "389125467"

if __name__ == "__main__":
    cups = get_data(day=23, year=2020)

    next_cup = play_game([int(num) for num in cups], 100, len(cups))
    res = ""
    n = 1
    for _ in range(len(cups)):
        n = next_cup[n]
        res += str(n)
    print(res)

    next_cup = play_game([int(num) for num in cups], 10 ** 7, 10 ** 6)
    first = next_cup[1]
    second = next_cup[first]
    print(first, second)
    print(first * second)
