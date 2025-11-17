import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import heapq

WALL_NUM = 10000

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        if test:
            self.rows = 7
            self.cols = 7
        else:
            self.rows = 71
            self.cols = 71
        self.lines = self.file.splitlines()
        self.grid = np.ones((self.rows, self.cols))
        for ii, line in enumerate(self.lines):
            if test and ii < 12:
                (y, x) = line.split(',')
                self.grid[int(x), int(y)] = WALL_NUM
            elif not test and ii < 1024:
                (y, x) = line.split(',')
                self.grid[int(x), int(y)] = WALL_NUM
        print(self.grid)

    def check_bounds(self, point):
        (x, y) = point
        if 0 <= x < self.rows and 0 <= y < self.cols: return True
        else: return False

    def dijkstra(self):
        distances = np.full((self.rows, self.cols), np.inf)
        distances[self.start] = 0
        parents = {self.start: None}
        # Priority queue for (distance, (row, col))
        queue = [(0, self.start)]
        seats = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            current_distance, (current_row, current_col) = heapq.heappop(queue)
            if (current_row, current_col) == self.end:
                break
            if current_distance > distances[current_row, current_col]:
                continue
            for dir in directions:
                neighbor_row, neighbor_col = current_row + dir[0], current_col + dir[1]
                if self.check_bounds((neighbor_row, neighbor_col)):
                    distance = current_distance + self.grid[neighbor_row, neighbor_col]
                    if distance < distances[neighbor_row, neighbor_col]:
                        distances[neighbor_row, neighbor_col] = distance
                        parents[(neighbor_row, neighbor_col)] = (current_row, current_col)
                        heapq.heappush(queue, (distance, (neighbor_row, neighbor_col)))
        
        path = set()
        current = self.end
        while current is not None:
            path.add(current)
            current = parents.get(current)
        return path, int(distances[self.end]), distances
 

    def silver(self):
        self.start = (0, 0)
        self.end = (self.cols-1, self.rows-1)
        path, cost, distances = self.dijkstra()
        # Remove the first (0,0) from path and return
        for ii in range(0, self.cols):
            str_to_print = ''
            for jj in range(0, self.rows):
                if (ii, jj) in path:
                    str_to_print += 'x'
                else:
                    str_to_print += '.'
            print(str_to_print)
        return len(path)-1

    def gold(self):
        '''
        Loop through the data adding one at a time and running dijkstra.
        '''
        self.start = (0, 0)
        self.end = (self.cols-1, self.rows-1)
        idx = 1
        while True:
            bytes = set()
            self.grid = np.ones((self.rows, self.cols))
            for ii in range(0, idx):
                line = self.lines[ii]
                (y, x) = line.split(',')
                self.grid[int(x), int(y)] = WALL_NUM
                bytes.add((int(x), int(y)))
            path, cost, distances = self.dijkstra()
            if path.intersection(bytes):
                # Return the last line added to grid
                return line
            else:
                idx += 1


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
