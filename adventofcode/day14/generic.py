from collections import defaultdict
from typing import List

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def apply_mask_v1(mask, value):
    binary = f"{value:036b}"
    return int(
        "".join(
            [
                bit if mask[index] == "X" else mask[index]
                for index, bit in enumerate(binary, 0)
            ]
        ),
        2,
    )


def initialize_docking_v1(input: List[str]):
    mask = "X" * 36
    memory = defaultdict(int)
    for inst in input:
        if "mem" in inst:
            index, value = inst.split("=")
            index = int(index.lstrip("mem[").rstrip("] "))
            value = int(value.strip())
            memory[index] = apply_mask_v1(mask, value)
        if "mask" in inst:
            mask = inst.split("=")[-1].strip()
    print(sum(memory.values()))

def apply_mask_v2(mask, value):
    binary = f"{value:036b}"
    flts = mask.count("X")
    results = []
    for i in range(2 ** flts):
        flt_val = list(f"{i:036b}")
        res = ""
        for index, bit in enumerate(mask, 0):
            if bit == "0":
                res += binary[index]
            if bit == "1":
                res += "1"
            if bit == "X":
                res += flt_val.pop(-1)
        results.append(int(res, 2))
    return results

def initialize_docking_v2(input: List[str]):
    mask = "0" * 36
    memory = defaultdict(int)
    for inst in input:
        if "mem" in inst:
            index, value = inst.split("=")
            index = int(index.lstrip("mem[").rstrip("] "))
            value = int(value.strip())
            indicies = apply_mask_v2(mask, index)
            for mapped_index in indicies:
                memory[mapped_index]= value
        if "mask" in inst:
            mask = inst.split("=")[-1].strip()
    print(sum(memory.values()))


if __name__ == "__main__":
    input = get_data(day=14, year=2020).splitlines()
    initialize_docking_v1(input)
    initialize_docking_v2(input)
