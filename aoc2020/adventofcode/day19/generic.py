from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def check(grammar, indicies, string):
    if not indicies:
        yield string
    else:
        # replace the first index with the rule it references and parse
        index, *indicies = indicies
        for string in run(grammar, index, string):
            yield from check(grammar, indicies, string)


def expand(grammar, options, string):
    # iterate through the possible options for this sequence
    for option in options:
        yield from check(grammar, option, string)


def run(grammar, index, string):
    # if the rule is a reference to more rules keep parsing
    if isinstance(grammar[index], list):
        yield from expand(grammar, grammar[index], string)
    else:
        # if there is a a character left and it matches the rule
        if string and string[0] == grammar[index]:
            # strip the first char and yield the rest to keep parsing
            # eventually the whole string will be gone and we will 
            yield string[1:]


def match(grammar, string):
    # parse thorugh the 
    return any(m == "" for m in run(grammar, "0", string))


def build_rules(input: str, loop: bool = False):
    rules = {}
    for line in input.splitlines():
        index, rule = line.split(": ")
        if rule[0] == '"':
            rules[index] = rule[1:-1]
        elif "|" in rule:
            rules[index] = [option.split() for option in rule.split(" | ")]
        else:
            rules[index] = [rule.split()]
    if loop:
        rules["8"] = [["42"], ["42", "8"]]
        rules["11"] = [["42", "31"], ["42", "11", "31"]]
    return rules


if __name__ == "__main__":
    rules, messages = get_data(day=19, year=2020).split("\n\n")
    rules = build_rules(rules, loop=True)
    print(sum(match(rules, message) for message in messages.splitlines()))