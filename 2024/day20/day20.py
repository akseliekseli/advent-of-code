import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import functools
import heapq

WALL_NUM = 100000

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.grid = []
        self.walls = []
        for ii, line in enumerate(self.lines):
            self.grid.append([])
            for jj, char in enumerate(line):
                if char=='#':
                    self.grid[ii].append(WALL_NUM)
                    self.walls.append((ii, jj))
                else:
                    if char=='S': self.start = (ii, jj)
                    elif char=='E': self.end = (ii, jj)
                    self.grid[ii].append(1)
        self.grid = np.array(self.grid, dtype=float)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

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
        path, cost_initial, distances = self.dijkstra()
        saves = []
        # For horizontal cheats
        n_walls = len(self.walls)
        for ii, wall in enumerate(self.walls):
            if wall[0] >0 and wall[0] < self.rows-1 and wall[1] > 0 and wall[1] < self.cols-1:
                self.grid[wall] = 1
                path, cost_new, distances = self.dijkstra()
                if cost_new < cost_initial:
                    saves.append(cost_initial - cost_new)
                self.grid[wall] = WALL_NUM
            print(f'Iteration: {ii+1}/{n_walls}')
        
        result = len([x for x in saves if x>=100])
        return result

    def calculate_longer_cheats(self):
        for ii in range(0, self.MAX_CHEAT):
            for jj in range(0, self.MAX_CHEAT):
                pass 
        
        pass

    def gold(self):
        self.MAX_CHEAT = 20
        path, cost, distances = self.dijkstra()
        print(path)
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
