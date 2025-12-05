import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time


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
        fresh_set = set()
        num_fresh = 0
        for ii, line in enumerate(self.lines):
            if line == "":
                continue

            if line.find("-") != -1:
                a, b = line.split("-")
                a, b = int(a), int(b)
                fresh_set.add((a, b))
            else:
                c = int(line)
                for fs in fresh_set:
                    if c <= fs[1] and c >= fs[0]:
                        num_fresh += 1
                        break
        print(fresh_set)
        return num_fresh

    def merge_overlapping(self, arr):
        # Merge overlapping intervals in list of lists
        # Also now created a help function for future

        # sort based on the start
        arr.sort()
        res = []
        res.append(arr[0])
        for i in range(1, len(arr)):
            last = res[-1]
            curr = arr[i]
            # Merge, if current interval overlaps with the last merged
            if curr[0] <= last[1]:
                last[1] = max(last[1], curr[1])
            else:
                res.append(curr)

        return res

    def gold(self):
        fresh_list = []
        num_fresh = 0
        for ii, line in enumerate(self.lines):
            if line == "":
                break
            if line.find("-") != -1:
                a, b = line.split("-")
                fresh_list.append([int(a), int(b)])

        merged = self.merge_overlapping(fresh_list)
        for m in merged:
            num_fresh += m[1] - m[0] + 1  # Add 1: [3,5] 5-3 = 2, range is 3
        return num_fresh


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
