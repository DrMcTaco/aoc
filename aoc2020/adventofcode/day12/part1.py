from dataclasses import dataclass

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Ship:
    theta: int = 0
    x: int = 0
    y: int = 0

    def __post_init__(self):
        self.history = [(self.x, self.y, self.theta)]

    def N(self, val):
        self.y += val
        self.history.append((self.x, self.y, self.theta))

    def S(self, val):
        self.y -= val
        self.history.append((self.x, self.y, self.theta))

    def E(self, val):
        self.x += val
        self.history.append((self.x, self.y, self.theta))

    def W(self, val):
        self.x -= val
        self.history.append((self.x, self.y, self.theta))

    def L(self, val):
        self.theta += val
        self.history.append((self.x, self.y, self.theta))

    def R(self, val):
        self.theta -= val
        self.history.append((self.x, self.y, self.theta))

    def F(self, val):
        if self.theta % 360 == 0:
            self.x += val
        elif self.theta % 360 == 90:
            self.y += val
        elif self.theta % 360 == 180:
            self.x -= val
        elif self.theta % 360 == 270:
            self.y -= val

        self.history.append((self.x, self.y, self.theta))

    def process_inst(self, inst):
        self.__getattribute__(inst[0])(int(inst[1:]))


if __name__ == "__main__":
    data = get_data(day=12, year=2020)
    boat = Ship()
    for inst in data.splitlines():
        boat.process_inst(inst)

    print(sum([abs(val) for val in boat.history[-1][0:2]]))
