import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time

'''
Today was nice. The gold task modification was a bug I had in the first tast :DD
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()

    def first(self):
        self.rows = len(self.lines)
        self.matrix = []
        zero_map = []
        for ii, line in enumerate(self.lines):
            self.cols = len(line)
            self.matrix.append([int(item) for item in line])
            for jj, num in enumerate(line):
                if int(line[jj]) == 0:
                    zero_map.append((ii, jj))
        
        # Compute all the different trails from zeros to 9s
        trailheads = 0
        map_temp = copy.deepcopy(zero_map)
        for zero in zero_map:
            for ii in range(1, 10):
                zero = self.check_next(zero, ii)
            # Zero to set so I get only the coordinates of 9s
            trailheads += len(set(zero))

        return trailheads

    def check_next(self, points, next):
        '''
        Get coordinates of neighbors, which have the next value
        '''
        l =  [] 
        # Check if multiple points in points
        if isinstance(points, list):
            for point in points:
                neighbors = self.get_neighbors(point)
                for neig in neighbors:
                    if self.matrix[neig[0]][neig[1]] == next:
                        l.append(neig)
        else:
            neighbors = self.get_neighbors(points)
            for neig in neighbors:
                if self.matrix[neig[0]][neig[1]] == next:
                    l.append(neig)

        return l
    
    def get_neighbors(self, point):
        # Use a kernel to calculate next points and check if they are inbounds
        x, y = point
        self.kernel = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in self.kernel]
        neighbors = [(x, y) for x, y in neighbors if self.check_bounds((x, y))]
        return neighbors

    def get_next_num(self):
        for ii in range(1, 10): yield ii 

    def check_bounds(self, point):
        (x, y) = point
        if 0 <= x < self.rows and 0 <= y < self.cols: return True

    def second(self):
        self.rows = len(self.lines)
        self.matrix = []
        zero_map = []
        for ii, line in enumerate(self.lines):
            self.cols = len(line)
            self.matrix.append([int(item) for item in line])
            for jj, num in enumerate(line):
                if int(line[jj]) == 0:
                    zero_map.append((ii, jj))
        trailheads = 0
        map_temp = copy.deepcopy(zero_map)
        for zero in zero_map:
            for ii in range(1, 10):
                zero = self.check_next(zero, ii)
            # Just didn't change zero to set, so I got all the trails
            trailheads += len(zero)

        return trailheads


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.first() if case == 1 else solution.second()
    end = time.time()
    print(f'Results part {case}: {results}')
    print(f'Runtime: {end-start}')
