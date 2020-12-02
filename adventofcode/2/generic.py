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
    def is_valid_count(self):
        return (
            self.policy.minimum
            <= self.password.count(self.policy.character)
            <= self.policy.maximum
        )

    @property
    def is_valid_position(self):
        return (self.password[self.policy.minimum  -1] == self.policy.character) ^ (
            self.password[self.policy.maximum - 1] == self.policy.character
        )


def main(raw_passwords: str):
    passwords = [Password.from_string(pw) for pw in raw_passwords.splitlines()]
    print(f"Valid by count: {sum([int(password.is_valid_count) for password in passwords])}")
    print(f"Valid by position: {sum([int(password.is_valid_position) for password in passwords])}")

if __name__ == "__main__":
    raw_passwords = Path("passwords.txt").open().read()
    main(raw_passwords)
