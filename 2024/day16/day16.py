import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict, deque
import time
import heapq

WALL_NUM = 100000

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.grid = []
        for ii, line in enumerate(self.lines):
            self.grid.append([])
            for jj, char in enumerate(line):
                if char=='#':
                    self.grid[ii].append(WALL_NUM)
                else:
                    if char=='S': self.start = (ii, jj)
                    elif char=='E': self.end = (ii, jj)
                    self.grid[ii].append(1)
        self.grid = np.array(self.grid, dtype=float)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])


    def dijkstra(self):
        distances = np.full((self.rows, self.cols), np.inf)
        distances[self.start] = 0
        parents = {self.start: None}
        visited = defaultdict()
        # Priority queue for (distance, (row, col), prev_dir)
        queue = [(0, self.start, None)]
        seats = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            current_distance, (current_row, current_col), prev_dir = heapq.heappop(queue)
            if (current_row, current_col) == self.end:
                break
            if current_distance > distances[current_row, current_col]:
                continue
            for dir in directions:
                neighbor_row, neighbor_col = current_row + dir[0], current_col + dir[1]
                if self.check_bounds((neighbor_row, neighbor_col)):
                    distance = current_distance + self.grid[neighbor_row, neighbor_col]
                    if prev_dir is not None and dir != prev_dir:
                        distance += 1000
                    if distance < distances[neighbor_row, neighbor_col]:
                        distances[neighbor_row, neighbor_col] = distance
                        parents[(neighbor_row, neighbor_col)] = (current_row, current_col)
                        heapq.heappush(queue, (distance, (neighbor_row, neighbor_col), dir))
        path = []
        current = self.end
        while current is not None:
            path.append(current)
            current = parents.get(current)
        path.reverse()
        return path, int(distances[self.end]), distances
     
    def get_neighbors(self, x, y):
        """
        Get all valid neighbors for a cell in the grid.

        :param x: Row index of the current cell
        :param y: Column index of the current cell
        :return: List of valid neighbor cells (x, y)
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 1:
                neighbors.append(((nx, ny), (dx, dy)))
        return neighbors
    
    def dijkstra_gold(self):
        distances = np.full((self.rows, self.cols), np.inf)
        distances[self.start] = 0
        parents = {self.start: None}
        seats = {self.start}
        visited = set()
        best_score = np.inf
        # Priority queue for (distance, (row, col), prev_dir)
        queue = [(0, self.start, None, [self.start])]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            current_distance, (current_row, current_col), prev_dir, path = heapq.heappop(queue)
            if current_distance > best_score:
                return seats
            visited.add(((current_row, current_col), prev_dir))
            for dir in directions:
                neighbor_row, neighbor_col = current_row + dir[0], current_col + dir[1]
                distance = current_distance + self.grid[neighbor_row, neighbor_col]
                if self.check_bounds((neighbor_row, neighbor_col)):
                    if prev_dir is not None and dir != prev_dir:
                        distance += 1000
                    if ((neighbor_row, neighbor_col), dir) in visited:
                        continue
                    if (current_row, current_col) == self.end:
                        best_score = current_distance
                        seats.update(path + [(current_row, current_col)])
                    elif distance < distances[(neighbor_row, neighbor_col)]:
                        path_new = path + [(neighbor_row, neighbor_col)]
                        heapq.heappush(queue, (distance, (neighbor_row, neighbor_col), dir, path_new))
     
    def compute_path(self, parents):
        path = []
        current = self.end
        while current is not None:
            path.append(current)
            current = parents.get(current)
        path.reverse()
        return path

    def check_bounds(self, point):
        (x, y) = point
        if self.grid[x][y] == WALL_NUM: return False
        if 0 <= x < self.rows and 0 <= y < self.cols: return True
        else: return False

    def silver(self):
        path, score, distances = self.dijkstra() 
        print(path)
        return score+1000

    def gold(self):
        seats = self.dijkstra_gold() 
        for ii in range(0, self.rows):
            print_row = ''
            for jj in range(0, self.cols):
                if (ii, jj) in seats:
                    print_row += 'O'
                else: print_row += self.lines[ii][jj]
            print(print_row)
        return len(seats)

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
