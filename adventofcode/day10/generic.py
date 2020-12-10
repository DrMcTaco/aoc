from collections import defaultdict
from typing import List

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def get_valid_nexts(value: int, adapters):
    return set(range(value + 1, value + 4)).intersection(adapters)


def build_clusters(input):
    # separate values into cluster by splitting on value-n - value-n+1 == 3
    input.sort()
    clusters = defaultdict(list)
    clusters[0].append(0)
    cluster_index = 0
    for index, val in enumerate(input, 1):
        clusters[cluster_index].append(val)
        if index == len(input):
            continue
        if input[index] - val == 3:
            cluster_index += 1

    return clusters


def main(input: List[int]):
    clusters = build_clusters(input)
    input.append(0)
    input.sort()
    diffs = defaultdict(int)
    for index, adapter in enumerate(input[:-1], 1):
        diffs[input[index] - adapter] += 1
    diffs[3] += 1

    print(f"Result: {diffs[3] * diffs[1]}")

    def build_chain(val, inputs, result):
        # recursively build valid chains
        if 1 <= len(inputs) <= 2:
            # short circuit trivial cases
            result["combos"] = 1
            return
        nexts = get_valid_nexts(val, inputs)

        for adapter in nexts:
            if max(inputs) == adapter:
                result["combos"] += 1
                continue
            build_chain(adapter, inputs, result)


    results = {}

    for index, cluster in clusters.items():
        # compute number of valide permutations per cluster of nodes
        results[index] = {"combos": 0}
        build_chain(min(cluster), cluster, results[index])

    final = 1
    for res in results.values():
        final *= res["combos"]

    print(f"There are {final} valid adapter chains")


if __name__ == "__main__":
    data = get_data(day=10, year=2020)
    main([int(datum) for datum in data.splitlines()])