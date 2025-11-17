import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time


class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.locks = []
        self.keys = []
        cols = [-1, -1, -1, -1, -1]
        new = True
        for ii, line in enumerate(self.lines):
            if line == '':
                if lock: self.locks.append(cols)
                elif not lock: self.keys.append(cols)
                cols = [-1, -1, -1, -1, -1]
                new = True
                continue
            if new:
                if line == '#####': lock = True
                elif line == '.....': lock = False
                new = False
            for jj, char in enumerate(line):
                if char == '#':
                    cols[jj] += 1
        if lock: self.locks.append(cols)
        elif not lock: self.keys.append(cols)
        print(self.locks)
        print(self.keys)

    def silver(self):
        result = 0
        
        for lock in self.locks:
            for key in self.keys:
                if all(lock[ii] + key[ii] <= 5 for ii in range(0, 5)):
                    result += 1

        return result



    def gold(self):
        pass


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()
    end = time.time()
    print(f'Results part {case}: {results}')
    print(f'Runtime: {end-start}')
