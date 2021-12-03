from typing import  List, Tuple

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()


def play_game(
    player1: List[int], player2: List[int], recursive: bool = False
) -> Tuple[List[int], str]:
    history = set()
    while player1 and player2:
        winner = None
        state = (tuple(player1), tuple(player2))
        if recursive and state in history:
            return player1, "p1"
        history.add(state)
        p1, *player1 = player1
        p2, *player2 = player2
        if recursive and (p1 <= len(player1)) and (p2 <= len(player2)):
            _, winner = play_game(
                player1[:p1],
                player2[:p2],
                recursive=True,
            )
            if winner == "p1":
                player1.extend([p1, p2])
            else:
                player2.extend([p2, p1])
            continue

        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    if player1:
        winning_deck = player1
        winner = "p1"
    else:
        winning_deck = player2
        winner = "p2"

    return winning_deck, winner


if __name__ == "__main__":
    p1, p2 = get_data(day=22, year=2020).split("\n\n")
    winning_deck, _ = play_game(
        [int(card) for card in p1.splitlines()[1:]],
        [int(card) for card in p2.splitlines()[1:]],
    )
    print(sum([val * card for val, card in enumerate(reversed(winning_deck), 1)]))

    winning_deck, _ = play_game(
        [int(card) for card in p1.splitlines()[1:]],
        [int(card) for card in p2.splitlines()[1:]],
        True,
    )
    print(sum([val * card for val, card in enumerate(reversed(winning_deck), 1)]))
