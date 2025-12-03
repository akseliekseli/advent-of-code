import csv
import argparse
from os import remove
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
        max_joltages = []
        for ii, line in enumerate(self.lines):
            joltages = set()
            for jj in range(0, len(line) - 1):
                for kk in range(jj + 1, len(line)):
                    joltages.add(int(line[jj] + line[kk]))
            max_joltages.append(max(joltages))
        print(f" Max Joltages: {max_joltages}")
        return sum(max_joltages)

    def gold(self):
        max_joltages = []
        for ii, line in enumerate(self.lines):
            jj = len(line) - 12
            self.line_joltage = line[jj:]
            """
            The idea is
            1. go through the line backwards
            2. add the next number (len(new_line) == 13)
            3. remove kk number one by one and compare if larger
            """
            while jj > 0:
                new_line = line[jj - 1] + self.line_joltage
                for kk in range(0, len(new_line)):
                    removed_kk = new_line[:kk] + new_line[kk + 1 :]
                    if removed_kk >= self.line_joltage:
                        self.line_joltage = removed_kk
                jj -= 1
            max_joltages.append(int(self.line_joltage))
        print(f" Max Joltages: {max_joltages}")
        return sum(max_joltages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-test", help="True/False")
    parser.add_argument("-case", help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ["True", "true"] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()
    end = time.time()
    print(f"Results part {case}: {results}")
    print(f"Runtime: {end - start}")
