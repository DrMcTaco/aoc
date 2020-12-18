import re
from operator import mul, add

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

opp = {"+": add, "*": mul}


def basic_solve(section: str):
    parts = section.split()
    a = int(parts[0])
    action = opp[parts[1]]
    b = int(parts[2])
    a = action(a, b)
    if len(parts) > 3:
        i = 3
        while i < len(parts):
            action = opp[parts[i]]
            b = int(parts[i + 1])
            a = action(a, b)
            i += 2
    return a


def advanced_solve(section: str):
    add = re.search(r"\d+ \+ \d+", section)
    while add:
        res = eval(add.group())
        section = section.replace(add.group(), str(res), 1)
        add = re.search(r"\d+ \+ \d+", section)

    mul = re.search(r"\d+ \* \d+", section)
    while mul:
        res = eval(mul.group())
        section = section.replace(mul.group(), str(res), 1)
        mul = re.search(r"\d+ \* \d+", section)
    return int(section)


def do_math(section: str, advanced: bool = False):
    solve = basic_solve
    if advanced:
        solve = advanced_solve
    matches = re.findall(r"(\([^\(\)]+\))", section)
    while matches:
        for match in matches:
            res = solve(match.strip("(").strip(")"))
            section = section.replace(match, str(res), 1)
        matches = re.findall(r"(\([^\(\)]+\))", section)
    res = solve(section)
    return res


if __name__ == "__main__":
    input = get_data(day=18, year=2020)
    print(sum([do_math(problem) for problem in input.splitlines()]))
    print("part 2")
    print(sum([do_math(problem, advanced=True) for problem in input.splitlines()]))
