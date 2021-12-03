from itertools import combinations
from functools import reduce
from operator import mul
from pathlib import Path
from sys import argv
from typing import List, Union


def prep_report(report: str) -> List[str]:
    return [int(item) for item in report.splitlines() if item]


def prod(iterable: List[Union[int, float]]):
    """
    Pyhton <3.8 does not have a product fucntion
    Think sum but for multiplication
    """
    return reduce(mul, iterable)


def main(expense_report: str, number: int = 2):
    expenses = prep_report(expense_report)
    combos = combinations(expenses, number)
    for combo in combos:
        if sum(combo) == 2020:
            print(f"The elements {combo} sum to 2020.\nTheir product is: {prod(combo)}")


if __name__ == "__main__":
    report = Path("expense_report.txt")
    if len(argv) > 1:
        main(report.open().read(), int(argv[1]))
    else:
        main(report.open().read())