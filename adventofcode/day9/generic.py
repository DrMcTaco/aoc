from itertools import combinations
from typing import List

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

def check_valid(preamble: List[int], val: int):
    return (val in {sum(combo) for combo in combinations(preamble, 2)})

def find_invalid(input: List[int], preamble_len: int):
    preamble = input[0:preamble_len]
    for index, value in enumerate(input[preamble_len:], preamble_len):
        if not check_valid(preamble, value):
            print(f"{value} is not a valid number")
            return value
        preamble.pop(0)
        preamble.append(input[index])

def find_invalid_components(input: List[int], invalid_num: int):
    components = []
    for num in input:
        components.append(num)
        if sum(components) == invalid_num:
            return components
        elif sum(components) > invalid_num:
            while sum(components) > invalid_num:
                components.pop(0)
                if sum(components) == invalid_num:
                    return components
    raise RuntimeError("Did not find vulnerability")

def main(data_: List[int], preamble_len: int):
    invalid_num = find_invalid(data_, preamble_len)
    invalid_components = find_invalid_components(data_, invalid_num)
    print(f"The weakness is {min(invalid_components) + max(invalid_components)}")

t_data = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

if __name__ == "__main__":
    data = get_data(day=9, year=2020)
    main([int(datum) for datum in data.splitlines()], 25)