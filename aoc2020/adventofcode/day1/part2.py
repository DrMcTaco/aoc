from itertools import combinations
from pathlib import Path
from typing import List


def prep_report(report: str) -> List[str]:
    return [int(item) for item in report.splitlines() if item]

def main(expense_report: str):
    expenses = prep_report(expense_report)
    combos = combinations(expenses, 3)
    for a, b, c  in combos:
        if a + b + c == 2020:
            print(f"The elements {a}, {b}, and {c} sum to 2020.\nTheir product is: {a * b * c}")

if __name__ == "__main__":
    report = Path("expense_report.txt")
    main(report.open().read())