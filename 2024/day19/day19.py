import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
from functools import cache

'''
Utilizing cache for speedup. 
Recursive solution for silver that was then modified to compute all possibilities
for gold star.

Recursion found here: https://www.geeksforgeeks.org/python-check-if-given-string-can-be-formed-by-concatenating-string-elements-of-list/
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()

        self.patterns = set(item.strip() for item in self.lines[0].split(','))
        self.designs = list()

        for ii, line in enumerate(self.lines[2:]):
            self.designs.append(line)

    @cache
    def can_construct(self, remaining):
        if not remaining:
            return True
        for pattern in self.patterns:
            if remaining.startswith(pattern):
                if self.can_construct(remaining[len(pattern):]):
                    return True
        return False

    def silver(self):
        count = 0
        for ii, design in enumerate(self.designs):
            if self.can_construct(design):
                count += 1
            else: pass

        return count
    
    @cache
    def number_of_designs(self, remaining):
        if not remaining:
            return 1
        count = 0
        for pattern in self.patterns:
            if remaining.startswith(pattern):
                count += self.number_of_designs(remaining[len(pattern):])
        return count

    def gold(self):
        count = 0
        for ii, design in enumerate(self.designs):
            count += self.number_of_designs(design)
        return count


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
