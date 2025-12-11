import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import functools


def find_all_parents(G, s):
    Q = [s]
    parents = defaultdict(set)
    while len(Q) != 0:
        v = Q[0]
        Q.pop(0)
        for w in G.get(v, []):
            parents[w].add(v)
            Q.append(w)
    return parents


def find_all_paths(parents, a, b):
    return (
        [a]
        if a == b
        else [y + b for x in list(parents[b]) for y in find_all_paths(parents, a, x)]
    )


def count_paths_with_intermediates(graph, start, end, intermediates):
    # Found this template for DFS somewhere online and then extended it to
    # use memoization.
    # We save the path counts based on the node and the state (state is the intermediates visited)
    memo = {}
    intermediate_map = {node: i for i, node in enumerate(intermediates)}
    start_state = (0,) * len(intermediates)

    def dfs_count(current_node, state):
        if (current_node, state) in memo:
            return memo[(current_node, state)]
        new_state = list(state)
        if current_node in intermediate_map:
            index = intermediate_map[current_node]
            new_state[index] = 1
        new_state = tuple(new_state)
        if current_node == end:
            if all(new_state):
                return 1
            else:
                return 0
        count = 0
        for neighbor in graph.get(current_node, []):
            count += dfs_count(neighbor, new_state)
        memo[(current_node, state)] = count
        return count

    return dfs_count(start, start_state)


class Solution:
    input_filename = "input.txt"
    input_filename_test = "example.txt"

    def __init__(self, test=False):
        self.file = (
            open(self.input_filename_test, "r").read()
            if test
            else open(self.input_filename, "r").read()
        )
        self.lines = self.file.splitlines()

    def silver(self):
        """
        Simply BFS brute force and then get the correct paths
        """
        nodes = defaultdict(list)
        for ii, line in enumerate(self.lines):
            s = line.split(":")
            node = s[0]
            nodes[node].extend([n for n in s[1].split(" ")[1:]])
        return len(find_all_paths(find_all_parents(nodes, "you"), "you", "out"))

    def gold(self):
        """
        DFS where we keep track of visited intermediates.
        Speedup with memoization.
        """
        nodes = defaultdict(list)
        for ii, line in enumerate(self.lines):
            s = line.split(":")
            node = s[0]
            nodes[node].extend([n for n in s[1].split(" ")[1:]])

        count = count_paths_with_intermediates(
            nodes, "svr", "out", intermediates=["dac", "fft"]
        )
        return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="True/False")
    parser.add_argument("-c", help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.c)
    test = True if args.t in ["True", "true"] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()
    end = time.time()
    print(f"Results part {case}: {results}")
    print(f"Runtime: {end - start}")
