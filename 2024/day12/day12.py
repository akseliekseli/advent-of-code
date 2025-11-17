import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict, deque
import time


class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.rows = len(self.lines)
        self.cols = len(self.lines[0])

    def form_regions(self):
        '''
        This is a BFS "himmeli", that forms a dict with
        containing each region
        '''
        for ii, line in enumerate(self.lines):
            for jj, plant in enumerate(line):
                self.gardens[plant].append((ii,jj))

        regions = defaultdict(list)
        visited = set()

        for plant in self.gardens.keys():
            for point in self.gardens[plant]:
                if point not in visited:
                    reg_ii = len(regions)
                    queue = deque([point])
                    visited.add(point)

                    while queue:
                        current = queue.popleft()
                        regions[f"{plant}{reg_ii}"].append(current)

                        for neighbor in self.check_next(current, plant):
                            if neighbor not in visited:
                                visited.add(neighbor)
                                queue.append(neighbor)
        return regions

    def silver(self):
        self.gardens = defaultdict(list)
        self.regions = self.form_regions()
        areas = [len(ii) for ii in self.regions.values()] 

        result = 0
        for ii, region in enumerate(self.regions.keys()):
            per = self.perimeter(self.regions, region)
            result += areas[ii]*per
        return result
            
    def perimeter(self, regions, key):
        per = 0
        for point in regions[key]:
            per += self.compute_num_of_outer_sides(point, regions[key])
        return per

    def compute_num_of_outer_sides(self, point, region):
        # Use a kernel to calculate next points and check if they are inbounds
        x, y = point
        self.kernel = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in self.kernel]
        n = 0
        for neighbor in neighbors:
            if neighbor in region:
                n += 1
        return 4 - n

    def get_neighbors(self, point):
        # Use a kernel to calculate next points and check if they are inbounds
        x, y = point
        self.kernel = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in self.kernel]
        neighbors = [(x, y) for x, y in neighbors if self.check_bounds((x, y))]
        return neighbors

    def check_bounds(self, point):
        (x, y) = point
        if 0 <= x < self.rows and 0 <= y < self.cols: return True
        else: return False
    
    def check_next(self, points, key):
        '''
        Get coordinates of neighbors, which have the next value
        '''
        l =  [] 
        # Check if multiple points in points
        if isinstance(points, list):
            for point in points:
                neighbors = self.get_neighbors(point)
                for neig in neighbors:
                    if neig in self.gardens[key]:
                        l.append(neig)
        else:
            neighbors = self.get_neighbors(points)
            for neig in neighbors:
                if neig in self.gardens[key]:
                    l.append(neig)
        return l

    def get_diag_neighbors(self, point):
        self.kernel_diag = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        x, y = point
        return [(x + dx, y + dy) for dx, dy in self.kernel_diag]
    
    def get_neighbors_no_bound_check(self, point):
        x, y = point
        self.kernel = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        return [(x + dx, y + dy) for dx, dy in self.kernel]
    
    def compute_num_of_corners(self, key):
        '''
        We compare the neighbours to the diagonal neighbours.
        With some rules, we can deduct, if the point has a corner or not.

        The corners are computed for each diagonal of each point. There might be some optimization
        possible, but this works.
        '''
        corner_count = 0
        for point in self.regions[key]:
            neighbors = self.get_neighbors_no_bound_check(point)
            diag_neighbors = self.get_diag_neighbors(point)
            # Just one point has 4 edges
            if not set(neighbors).intersection(set(self.regions[key])):
                corner_count += 4
            else:
                for idx, diag in enumerate(diag_neighbors):
                    if diag in self.regions[key]:
                        # This is done to index the neighbors properly
                        if idx == 3:
                            idx2 = 0
                        else:
                            idx2 = idx+1
                        # Check an edge-case where the neighbors are not in the set, but the diagonal is
                        if (not neighbors[idx] in self.regions[key]) and (not neighbors[idx2] in self.regions[key]):
                            corner_count += 1
                        else: pass
                    else:
                        if idx == 3:
                            idx2 = 0
                        else:
                            idx2 = idx+1
                        if (not neighbors[idx] in self.regions[key]) and (not neighbors[idx2] in self.regions[key]):
                            corner_count += 1
                        elif (neighbors[idx] in self.regions[key]) and (neighbors[idx2] in self.regions[key]):
                            corner_count += 1
        return corner_count

    def gold(self):
        '''
        In this task we calculate the number of edges by computing
        the number of corners in the shape.
        '''
        self.gardens = defaultdict(list)
        self.regions = self.form_regions()
        areas = [len(ii) for ii in self.regions.values()] 
        
        result = 0
        for ii, region in enumerate(self.regions.keys()):
            corners = self.compute_num_of_corners(region) 
            result += areas[ii]*self.compute_num_of_corners(region) 
        return result


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
