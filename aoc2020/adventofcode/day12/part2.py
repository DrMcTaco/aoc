from math import sin, cos, radians
from dataclasses import dataclass

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Ship:
    x: int = 0
    y: int = 0
    wx: int = 10
    wy: int = 1

    def __post_init__(self):
        self.history = [(self.x, self.y, self.wx, self.wy)]

    def N(self, val):
        self.wy += val

    def S(self, val):
        self.wy -= val

    def E(self, val):
        self.wx += val

    def W(self, val):
        self.wx -= val

    def L(self, val):
        val = radians(val % 360)
        nx = round(self.wx * cos(val) - self.wy * sin(val))
        ny = round(self.wx * sin(val) + self.wy * cos(val))
        self.wx = nx
        self.wy = ny

    def R(self, val):
        val = radians(-val % 360)
        nx = round(self.wx * cos(val) - self.wy * sin(val))
        ny = round(self.wx * sin(val) + self.wy * cos(val))
        self.wx = nx
        self.wy = ny

    def F(self, val):
        self.x += self.wx * val
        self.y += self.wy * val

    def process_inst(self, inst):
        self.__getattribute__(inst[0])(int(inst[1:]))
        self.history.append((self.x, self.y, self.wx, self.wy))


if __name__ == "__main__":
    data = get_data(day=12, year=2020)
    boat = Ship()
    for inst in data.splitlines():
        boat.process_inst(inst)

    print(sum([abs(val) for val in boat.history[-1][0:2]]))
