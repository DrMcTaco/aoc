from typing import List
from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def say(turns: List[int]):
    recent = turns[-1]
    try:
        # with every turn except the most recent in reversed order find the index of the value
        return turns[:-1][::-1].index(recent) + 1
    except ValueError:
        return 0


def play_game_naieve(start: List[int], turns):
    history = []
    for turn_no in range(turns):
        if turn_no < len(start):
            history.append(start[turn_no])
        else:
            history.append(say(history))
    print(history[-1])


def play_game_clever(start: List[int], turns):
    numbers = {value: index for index, value in enumerate(start[:-1], 0)}
    prev = start[-1]
    for i in range(len(start), turns):
        last_seen_at = numbers.get(prev)
        numbers[prev] = i - 1
        if last_seen_at == None:
            prev = 0
        else:
            prev = i - last_seen_at - 1
    print(prev)


t_data = "0,3,6"

if __name__ == "__main__":
    input = [int(num) for num in get_data(day=15, year=2020).split(",")]
    # input = [int(num) for num in t_data.split(",")]
    play_game_naieve(input, 2020)
    play_game_clever(input, 30000000)