import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import math

"""
Forgot to put alarm so a bit late today.

Luckily problem was quite easy.
"""


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
        problems = []
        count = 0
        for ii, line in enumerate(self.lines[:-1]):
            splitted = line.split(" ")
            splitted = [item for item in splitted if item != ""]
            for jj, num in enumerate(splitted):
                if ii == 0:
                    problems.append([])
                problems[jj].append(int(num))
        symbols = self.lines[-1].split(" ")
        symbols = [item for item in symbols if item != ""]
        for ii, symbol in enumerate(symbols):
            if symbol == "*":
                count += math.prod(problems[ii])
            elif symbol == "+":
                count += sum(problems[ii])

        return count

    def gold(self):
        """
        Fixed length rows so use that to parse the numbers to lists
        Then go through list and finally symbols
        """
        problems = ["" for ii in range(0, len(self.lines[0]))]
        count = 0
        for ii, line in enumerate(self.lines[:-1]):
            for jj, char in enumerate(line):
                problems[jj] += char

        problems_parsed = [[]]
        for ii, num in enumerate(problems):
            num = num.strip()
            if num.isnumeric():
                problems_parsed[-1].append(int(num))
            else:
                problems_parsed.append([])
        problems = problems_parsed
        symbols = self.lines[-1].split(" ")
        symbols = [item for item in symbols if item != ""]
        for ii, symbol in enumerate(symbols):
            if symbol == "*":
                count += math.prod(problems[ii])
            elif symbol == "+":
                count += sum(problems[ii])

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
