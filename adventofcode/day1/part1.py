from itertools import combinations
from pathlib import Path
from typing import List


def prep_report(report: str) -> List[str]:
    return [int(item) for item in report.splitlines() if item]

def main(expense_report: str):
    expenses = prep_report(expense_report)
    combos = combinations(expenses, 2)
    for a,b in combos:
        if a + b == 2020:
            print(f"The elements {a} and {b} sum to 2020.\nTheir product is: {a * b}")

if __name__ == "__main__":
    report = Path("expense_report.txt")
    main(report.open().read())