from string import ascii_lowercase

from aocd import get_data
from dotenv import load_dotenv

from adventofcode.day4.part1 import pares_inputs

load_dotenv()


letters = set(ascii_lowercase)


def count_any_yes(input: str):
    return len(letters.intersection(set(input)))


def count_all_yes(input: str):
    return len(letters.intersection(*[set(resp) for resp in input.split()]))

def main(data: str):
    # separate each group into a strin
    # make a set of chars in the strin
    # take set diff of lowecase letters with group response
    # subtract diff from 26 to get number of `yes` answers
    num_any_yes = sum([count_any_yes(input) for input in pares_inputs(data)])
    num_all_yes = sum([count_all_yes(input) for input in pares_inputs(data)])

    print(f"There were {num_any_yes} yes asnwers where any memebr of a group anserwed")
    print(f"There were {num_all_yes} yes asnwers where any memebr of a group anserwed")


if __name__ == "__main__":
    data = get_data(day=6, year=2020)
    main(data)