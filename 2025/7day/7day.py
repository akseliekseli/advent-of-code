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
        beam_indices = {self.lines[0].index("S")}
        count = 0
        for ii, line in enumerate(self.lines[1:]):
            splitter_idx = set(filter(lambda i: line[i] == "^", range(len(line))))
            if splitter_idx == -1:
                continue
            temp = set()
            for idx in splitter_idx:
                if idx in beam_indices:
                    count += 1
                    temp.add(idx - 1)
                    temp.add(idx + 1)
                    beam_indices.remove(idx)
            beam_indices = beam_indices.union(temp)
        return count

    def gold(self):
        """
        Change to defaultdict to keep track of beam indices
        """
        beam_start = self.lines[0].index("S")
        beams = defaultdict(int)
        beams[beam_start] = 1
        for ii, line in enumerate(self.lines[1:]):
            splitter_idx = set(filter(lambda i: line[i] == "^", range(len(line))))
            temp = defaultdict(int)
            print(splitter_idx)
            if splitter_idx == set():
                continue
            splitted = []
            for idx in splitter_idx:
                if idx in beams.keys():
                    temp[idx - 1] += beams[idx]
                    temp[idx + 1] += beams[idx]
                    splitted.append(idx)
            not_splitted = [key for key in beams.keys() if key not in splitted]
            for key in not_splitted:
                temp[key] += beams[key]
            beams = temp
        return sum([count for _, count in beams.items()])

    def gold_better_from_reddit(self):
        """
        Found from reddit. Same idea as in my code, but done
        way nicer. With this way no need to keep track of the splitted/not splitted

        Could also easily do the silver with this by just
        increasing the count in if "^"

        We keep track of the beam based on index and compute
        how many ways you can get the beam to that index
        The dict keys are beam index and items the number of ways to come there
        Each split makes a new key where the items is the sum of the merging beams.
        """
        beam_start = self.lines[0].index("S")
        beams = defaultdict(int)
        beams[beam_start] = 1
        for ii, line in enumerate(self.lines[1:]):
            new_beams = defaultdict(int)
            for beam in beams:
                if line[beam] == "^":
                    new_beams[beam - 1] += beams[beam]
                    new_beams[beam + 1] += beams[beam]
                else:
                    new_beams[beam] += beams[beam]
            beams = new_beams
            print(beams)
        return sum([count for _, count in beams.items()])


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
