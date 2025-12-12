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

    def parse_data(self):
        self.presents = defaultdict(list)
        self.regions = defaultdict(list)

        regions_pattern = r"^(\d+)x(\d+):\s*(.*)$"

        for ii, line in enumerate(self.lines):
            if line == "":
                continue
            elif "x" in line:
                match = re.match(regions_pattern, line)
                cols = int(match.group(1))
                rows = int(match.group(2))
                data_str = match.group(3)
                # list of all presents needed (including duplicates)
                data_list = [
                    int(idx)
                    for idx, n in enumerate(data_str.split())
                    if int(n) > 0
                    for _ in range(int(n))
                ]
                self.regions[(cols, rows)].append(data_list)
            elif ":" in line:
                key = int(line[:-1])
                grid = [
                    [1 if x == "#" else 0 for x in row]
                    for row in self.lines[ii + 1 : ii + 4]
                ]
                self.presents[key] = grid

    def rotate_matrix(self, matrix):
        return [list(x) for x in zip(*matrix[::-1])]

    def silver(self):
        """
        Got this correct by accident and then needed to figure out why :D

        Drew the combinations for two presents and figured that most of them
        have the minimum area of 3x6 with some 3x5 and 4x4. The first idea was
        to do some mapping to these areas and run some search.

        I did this area computation just to check with the website, that this is
        indeed the upper bound for the solution (you have free space, but the presents
        cannot fit due to the shape).

        Turns out there are two types of present/region combos:
        - Region is much larger than what the presents take space
        - Region is smaller than what the presents take space

        -> By just taking the positive regions, you get the solution.

        Feeling trolled atm :DD
        """
        self.parse_data()
        count = 0
        for region in self.regions.keys():
            for presents in self.regions[region]:
                col, row = region
                area = col * row
                print(area)
                for present in presents:
                    present = np.array(self.presents[present])
                    area -= np.sum(present)
                if area > 0:
                    print(region, presents, area)
                    count += 1
        return count

    def gold(self):
        return


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
