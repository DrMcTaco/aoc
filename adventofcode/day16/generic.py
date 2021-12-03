from dataclasses import dataclass
from typing import List

from aocd import get_data
from dotenv import load_dotenv

from adventofcode.day1.generic import prod

load_dotenv()


@dataclass
class Rule:
    name: str
    conditions: List[tuple]
    potential_pos: set
    pos: int = None

    def check(self, value: int):
        for condition in self.conditions:
            if condition[0] <= value <= condition[1]:
                return True
        return False


@dataclass
class Scanner:
    rules: List[Rule]

    @classmethod
    def from_string(cls, input: str):
        num_rules = len(input.splitlines())
        rules = []
        for line in input.splitlines():
            name, raw_conditions = line.split(": ")
            conditions = []
            for condition in raw_conditions.split(" or "):
                low, high = condition.split("-")
                conditions.append((int(low), int(high)))
            rules.append(Rule(name, conditions, set(range(num_rules))))
        return cls(rules)

    def get_ticket_errors(self, ticket: str):
        errors = []
        for number in ticket.split(","):
            valid = False
            for rule in self.rules:
                if rule.check(int(number)):
                    valid = True
                    continue
            if not valid:
                errors.append(int(number))
        return errors

    def update_positions(self, fixed_pos):
        for rule in [x for x in self.rules if x.pos == None]:
            rule.potential_pos -= {fixed_pos}
            if len(rule.potential_pos) == 1:
                rule.pos = rule.potential_pos.pop()
                self.update_positions(rule.pos)

    def order_parts(self, ticket):
        for index, number in enumerate(ticket.split(","), 0):
            number = int(number)
            for rule in self.rules:
                if rule.pos != None:
                    continue
                if not rule.check(number):
                    rule.potential_pos -= {index}
                    if len(rule.potential_pos) == 1:
                        rule.pos = rule.potential_pos.pop()
                        self.update_positions(rule.pos)


if __name__ == "__main__":
    rules, my_ticket, tickets = get_data(day=16, year=2020).split("\n\n")
    scanner = Scanner.from_string(rules)
    errors = []
    for ticket in tickets.splitlines()[1:]:
        error = None
        error = scanner.get_ticket_errors(ticket)
        if not error:
            scanner.order_parts(ticket)
        else:
            errors.extend(error)
    print(sum(errors))
    my_values = my_ticket.splitlines()[1].split(",")
    target_indicies = [rule.pos for rule in scanner.rules if "departure" in rule.name]
    print(prod([int(my_values[index]) for index in target_indicies]))