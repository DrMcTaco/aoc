from collections import defaultdict
from dataclasses import dataclass, field
from typing import List

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Computer:
    instructions: List
    stack_pointer: int = field(default=0, init=False)
    accumulator: int = field(default=0, init=False)
    stop: bool = field(default=False, init=False)
    exec_count: dict = field(default_factory=lambda: defaultdict(int), init=False)
    exit_code: int = field(default=0, init=False)

    def acc(self, arg: int):
        self.accumulator += arg
        self.stack_pointer += 1

    def jmp(self, offset: int):
        self.stack_pointer += offset

    def nop(self, arg: int):
        self.stack_pointer += 1

    def execute_inst(self):
        self.exec_count[self.stack_pointer] += 1
        if self.exec_count[self.stack_pointer] > 1:
            self.stop = True
            self.exit_code = 1
            return
        inst, arg = self.instructions[self.stack_pointer].split()
        self.__getattribute__(inst)(int(arg))

    def run(self):
        while not self.stop:
            self.execute_inst()
            if self.stack_pointer >= len(self.instructions):
                self.stop = True

        print(
            f"the exit code is {self.exit_code} and the value of the accumulator is: {self.accumulator}"
        )
        return self.exit_code


def main(data_: str, fixloop: bool = True):
    if fixloop:
        jmp_nops = [
            index for index, inst in enumerate(data_, 0) if "jmp" in inst or "nop" in inst
        ]
        for index in jmp_nops:
            if "jmp" in data_[index]:
                data_[index] = data_[index].replace("jmp", "nop")
                comp = Computer(instructions=data_)
                ret = comp.run()
                data_[index] = data_[index].replace("nop", "jmp")
            else:
                data_[index] = data_[index].replace("nop", "jmp")
                comp = Computer(instructions=data_)
                ret = comp.run()
                data_[index] = data_[index].replace("jmp", "nop")

            if not ret:
                break
    else:
        comp = Computer(instructions=data_)
        ret = comp.run()


t_data = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

if __name__ == "__main__":
    data = get_data(day=8, year=2020)
    main(data.splitlines())