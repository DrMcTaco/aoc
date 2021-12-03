from dataclasses import dataclass
import re

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()
data = get_data(day=4, year=2020)


@dataclass
class Passport:
    byr: int = None
    iyr: int = None
    eyr: int = None
    hgt: int = None
    hcl: str = None
    ecl: str = None
    pid: str = None
    cid: str = None

    @classmethod
    def from_string(cls, input: str):
        return cls(**dict([field.split(":") for field in input.split()]))

    @property
    def is_valid(self):
        return bool(
            self.byr
            and self.iyr
            and self.eyr
            and self.hgt
            and self.hcl
            and self.ecl
            and self.pid
        )


def pares_inputs(input: str):
    """
    Split the input data into strings splitting on any number of blank lines.
    """
    blank_line_re = r"(?:\r?\n){2,}"
    return re.split(blank_line_re, input)


def main():
    passports = [Passport.from_string(input) for input in pares_inputs(data)]

    vaid_passports = sum([int(passport.is_valid) for passport in passports])
    print(f"There are {vaid_passports} valid passports")

if __name__ == "__main__":
    main()