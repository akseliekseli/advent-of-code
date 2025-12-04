import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
from scipy.signal import convolve2d


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
        Create 2d grid with 0 and 1 with 1s being the rolls.
        Use convolution to compute the sum of neighbouring elements -> how many rolls
        there are.
        Lastly filter.
        """
        self.grid = np.zeros((len(self.lines), len(self.lines[0])))
        for ii, line in enumerate(self.lines):
            for jj, element in enumerate(line):
                if element == "@":
                    self.grid[ii, jj] = 1
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        adjacent_rolls = convolve2d(
            self.grid, kernel, mode="same", boundary="fill", fillvalue=0
        )
        # THis didn't work
        # rolls = adjacent_rolls * self.grid
        return len(adjacent_rolls[(self.grid == 1) & (adjacent_rolls < 4)])

    def gold(self):
        """
        same as silver, but we count the rolls and then change them to 0 in
        the grid.
        """
        self.grid = np.zeros((len(self.lines), len(self.lines[0])))
        for ii, line in enumerate(self.lines):
            for jj, element in enumerate(line):
                if element == "@":
                    self.grid[ii, jj] = 1
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        removed_rolls = 0
        while True:
            adjacent_rolls = convolve2d(
                self.grid, kernel, mode="same", boundary="fill", fillvalue=0
            )
            new_possible_rolls = len(
                adjacent_rolls[(self.grid == 1) & (adjacent_rolls < 4)]
            )
            if new_possible_rolls == 0:
                return removed_rolls
            removed_rolls += new_possible_rolls
            self.grid[(self.grid == 1) & (adjacent_rolls < 4)] = 0


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
