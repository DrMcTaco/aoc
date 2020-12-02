from pathlib import Path
from dataclasses import dataclass


@dataclass
class PasswordPolicy:
    character: str
    minimum: int
    maximum: int


@dataclass
class Password:
    password: str
    policy: PasswordPolicy

    @classmethod
    def from_string(cls, string: str):
        quantity, char, raw = string.split()
        minimum, maximum = quantity.split("-")
        policy = PasswordPolicy(
            character=char.rstrip(":"), minimum=int(minimum), maximum=int(maximum)
        )
        return cls(raw, policy)

    @property
    def is_valid(self):
        return (
            self.policy.minimum
            <= self.password.count(self.policy.character)
            <= self.policy.maximum
        )


def main(raw_passwords: str):
    passwords = [int(Password.from_string(pw).is_valid) for pw in raw_passwords.splitlines()]
    print(sum(passwords))

if __name__ == "__main__":
    raw_passwords = Path("passwords.txt").open().read()
    main(raw_passwords)
