from pathlib import Path
from dataclasses import dataclass


@dataclass
class PasswordPolicy:
    character: str
    pos1: int
    pos2: int


@dataclass
class Password:
    password: str
    policy: PasswordPolicy

    @classmethod
    def from_string(cls, string: str):
        quantity, char, raw = string.split()
        pos1, pos2 = quantity.split("-")
        policy = PasswordPolicy(
            character=char.rstrip(":"), pos1=int(pos1), pos2=int(pos2)
        )
        return cls(raw, policy)

    @property
    def is_valid(self):
        return (self.password[self.policy.pos1  -1] == self.policy.character) ^ (
            self.password[self.policy.pos2 - 1] == self.policy.character
        )


def main(raw_passwords: str):
    passwords = [
        int(Password.from_string(pw).is_valid) for pw in raw_passwords.splitlines()
    ]
    print(sum(passwords))


if __name__ == "__main__":
    raw_passwords = Path("passwords.txt").open().read()
    main(raw_passwords)
