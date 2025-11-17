import csv
import argparse
import re
import numpy as np
from collections import defaultdict
import copy
import time

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.antennas = defaultdict(list)
        self.distance = lambda p1, p2: (p2[0] - p1[0], p2[1] - p1[1], p1)

    def data_to_matrix(self):
        matrix = []
        self.y_max = len(self.lines)
        for ii, line in enumerate(self.lines):
            self.x_max = len(line)
            for jj in range(len(line)):
                if line[jj] == '.':
                    pass
                else:
                    self.antennas[line[jj]].append((ii, jj))
            matrix.append(list(line))
        
        return matrix

    def first(self):
        self.matrix = self.data_to_matrix()
        self.compute_antinodes()
        in_bounds = {(x, y) for (x, y) in self.antinodes if self.check_bounds((x,y))}
        return len(in_bounds)

    def check_bounds(self, point):
        (x, y) = point
        if 0 <= x < self.x_max and 0 <= y < self.y_max: return True
        else: return False

    def compute_antinodes(self):
        self.antinodes = set() 
        for key, coords in self.antennas.items():
            for idx, point in enumerate(coords):
                results = [self.distance(p, point) for p in coords[idx+1:]]
                for res in results:
                    self.antinodes.add((point[0]+ res[0], point[1]+res[1]))
                    self.antinodes.add((res[2][0]- res[0], res[2][1]-res[1]))


    def second(self):
        self.matrix = self.data_to_matrix()
        self.compute_antinodes_gold()
        in_bounds = {(x, y) for (x, y) in self.antinodes if 0 <= x < self.x_max and 0 <= y < self.y_max}
        return len(in_bounds)

    def compute_antinodes_gold(self):
        self.antinodes = set() 
        for key, coords in self.antennas.items():
            for idx, point in enumerate(coords):
                results = [self.distance(p, point) for p in coords[idx+1:]]
                for res in results:
                    n = 0
                    while self.check_bounds((point[0]+ n*res[0], point[1] + n*res[1])) or self.check_bounds((res[2][0] - n*res[0], res[2][1] - n*res[1])): 
                        self.antinodes.add((point[0]+ n*res[0], point[1] + n*res[1]))
                        self.antinodes.add((res[2][0] - n*res[0], res[2][1]-n*res[1]))
                        n += 1
    

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
