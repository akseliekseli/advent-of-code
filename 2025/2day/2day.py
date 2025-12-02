import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import itertools


"""
Kivaa osallistua jokavuotiseen Luetunymmärtäminen-joulukalenteriin
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
        self.invalids = set()
        ranges = self.lines[0].split(",")
        for ii, ran in enumerate(ranges):
            a, b = ran.split("-")
            a, b = int(a), int(b)
            for num in range(a, b + 1):
                strnum = str(num)
                jj = len(strnum) // 2
                if strnum[0:jj] == strnum[jj:]:
                    self.invalids.add(num)
                    # print(f"added: {num}")
        return sum(self.invalids)

    def gold(self):
        self.invalids = set()
        ranges = self.lines[0].split(",")
        for ii, ran in enumerate(ranges):
            a, b = ran.split("-")
            a, b = int(a), int(b)
            for num in range(a, b + 1):
                tester = lambda s: re.match(r"(.+)\1+$", s)
                """
                Regex: 
                (.+)    ota yksi tai useampi merkki
                \1+     toista 1+ kertaa
                $       koko string oltava äsken toistettu pattern
                """
                if tester(str(num)):
                    self.invalids.add(num)
                    # print(f"added: {num}")
        return sum(self.invalids)

    def check_valid(self, s, a):
        # Luetunymmärtäminen :D
        substrings = [
            "".join(s[i:j]) for i, j in itertools.combinations(range(len(s) + 1), 2)
        ]
        for s in substrings:
            ii = len(s) // 2
            if s[0:ii] == s[ii:]:
                print(s)
                self.invalids.add(s)
        pass

    def check_palindrome(self, s):
        return any(c in s[i + 1 : i + 3] for i, c in enumerate(s))


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
