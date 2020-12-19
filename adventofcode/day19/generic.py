import re
from types import BuiltinFunctionType
from typing import Dict

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def resolve_rule(rule: str, rules: Dict[str, str]):
    if re.match(r"[^\d]", rule):
        return rule.strip('"')
    parts = rule.split(" | ")
    part_strs = []
    for part in parts:
        components = part.split()
        compstr = ""
        for component in components:
            compstr += resolve_rule(rules[component], rules)
        part_strs.append(compstr)
    res = "|".join(part_strs)
    return f"({res})" if "|" in res else res


def build_rules(input: str, loop: bool = False):
    rules = {}
    for line in input.splitlines():
        index, rule = line.split(": ")
        rules[index] = rule
    if loop:
        rules["8"] = "42 | 42 8"
        rules["11"] = "42 31 | 42 11 31"

    for index, rule in rules.items():
        rule = resolve_rule(rule, rules)
        rules[index] = rule
    return rules


t = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

d = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

if __name__ == "__main__":
    # rules, messages = get_data(day=19, year=2020).split("\n\n")
    rules, messages = d.split("\n\n")
    rules = build_rules(rules, loop=True)
    valid = 0
    for message in messages.splitlines():
        if re.fullmatch(rules["0"], message):
            valid += 1

    print(valid)