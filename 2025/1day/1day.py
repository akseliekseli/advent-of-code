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
        dial = 50
        count = 0
        for ii, line in enumerate(self.lines):
            dir, num = line[0], int(line[1:])
            # Change the left shifts to negative
            if dir == "L":
                num = -num
            dial = dial + num
            dial = dial % 100
            count += dial == 0
        return count

    def gold(self):
        dial = 50
        steps = 0
        count = 0
        for ii, line in enumerate(self.lines):
            dir, num = line[0], int(line[1:])
            if dir == "L":
                num = -num
            dial = dial + num
            dial = dial % 100
            print(dial)
            count += dial == 0
            # 2
            # Check if right wrap made. Exclude when dial is at 0
            print(num > 0 and dial < (num % 100) and dial != 0)
            steps += num > 0 and dial < (num % 100) and dial != 0
            # Check if left wrap made
            print(num < 0 and dial > 100 - (abs(num) % 100))
            steps += num < 0 and dial > 100 - (abs(num) % 100)
            # Multiple times around
            print(abs(num) // 100)
            steps += abs(num) // 100
            print(" ")
        return count + steps


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
