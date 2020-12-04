from dataclasses import dataclass
import re

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()
data = get_data(day=4, year=2020)


def hgt_valid(hgt: str):
    result = re.match(r"(?P<num>\d{2,3})(?P<unit>cm|in)", str(hgt))
    if result:
        if (result.group("unit") == "in" and 59 <= int(result.group("num")) <= 76) or (
            result.group("unit") == "cm" and 150 <= int(result.group("num")) <= 193
        ):
            return True
    return False

validators = {
        "byr": lambda x: 1921 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": hgt_valid,
        "hcl": lambda x: re.match(r"#([0-9a-f]{6})", str(x)),
        "ecl": lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
        "pid": lambda x: re.match(r"\d{9}", str(x)),
        "cid": lambda x: True,
}

@dataclass
class Passport:
    byr: int = None
    iyr: int = None
    eyr: int = None
    hgt: str = None
    hcl: str = None
    ecl: str = None
    pid: str = None
    cid: str = None

    

    @classmethod
    def from_string(cls, input: str):
        return cls(**dict([field.split(":") for field in input.split()]))

    @property
    def is_valid(self):
        for attr, func in validators.items():
            if attr != "cid" and not self.__getattribute__(attr):
                return False
            if not func(self.__getattribute__(attr)):
                return False
        return True


def pares_inputs(input: str):
    """
    Split the input data into strings splitting on any number of blank lines.
    """
    blank_line_re = r"(?:\r?\n){2,}"
    return re.split(blank_line_re, input)


passports = [Passport.from_string(input) for input in pares_inputs(data)]
valid_passports = sum([int(passport.is_valid) for passport in passports])
print(f"There are {valid_passports} valid passports")