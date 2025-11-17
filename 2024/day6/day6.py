import csv
import argparse
import re
import numpy as np
from collections import defaultdict
import copy
import time
import pickle
import matplotlib.pyplot as plt


'''
This day we learnt not to use try-except to check if indices are within the list bounds. :DD
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()

    def data_to_matrix(self):
        matrix = []
        y_bound = len(self.lines)
        for ii, line in enumerate(self.lines):
            for jj in range(len(line)):
                x_bound = len(line)
                if line[jj]=='^':
                    startpoint = [ii, jj]
            matrix.append(list(line))
        
        ii, jj = startpoint[0], startpoint[1]
        return matrix, ii, jj, y_bound, x_bound

    def first(self):
        self.matrix, ii, jj, self.rows, self.cols = self.data_to_matrix()
        matrix = copy.deepcopy(self.matrix)
        n_pos, matrix = self.traverse_matrix(matrix, ii, jj)
        return n_pos

    def traverse_matrix(self, input_matrix, ii, jj):
        '''
        This "himmeli" reminds me of Basics of Programming in Python course at LUT University
        '''
        dir = 0
        n_pos = 0
        self.loop = False
        matrix = copy.deepcopy(input_matrix)
        visited_points_dir = set()
        while (ii>=0) and (ii<self.rows) and (jj >=0) and (jj < self.cols):
            if ((ii, jj, dir)) in visited_points_dir:
                self.loop = True
                return n_pos, matrix
            else:
                visited_points_dir.add((ii, jj, dir)) 
            if self.check_bounds((ii, jj)):
                if dir==0:
                    if self.check_bounds((ii-1, jj)):
                        if matrix[ii-1][jj]=='#':
                            dir = 1
                        else:
                            ii -= 1
                            if matrix[ii][jj]=='X':
                                pass
                            else:
                                matrix[ii][jj]='X'
                                n_pos += 1
                    else:
                        break
                elif dir==1:
                    if matrix[ii][jj+1]=='#':
                        dir = 2
                    else:
                        jj += 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
                elif dir==2:
                    if matrix[ii+1][jj]=='#':
                        dir = 3
                    else:
                        ii += 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
                elif dir==3:
                    if self.check_bounds((ii, jj-1)):
                        if matrix[ii][jj-1]=='#':
                            dir = 0
                        else:
                            jj -= 1
                            if matrix[ii][jj]=='X':
                                pass
                            else:
                                matrix[ii][jj]='X'
                                n_pos += 1
                    else:
                        break
            else:
                break
        return n_pos, matrix
            
    def check_bounds(self, point):
        (x, y) = point
        if 0 <= x < self.x_max and 0 <= y < self.y_max: return True
        else: return False

    def second(self):
        self.matrix, starti, startj, self.rows, self.cols = self.data_to_matrix()
        self.x_max = self.rows-1
        self.y_max = self.cols-1
        _, m = self.traverse_matrix(self.matrix, starti, startj)
        xs = []
        for ii in range(0, self.rows):
            for jj in range(0, self.cols):
                if m[ii][jj] == 'X':
                    xs.append([ii, jj])
        loop_obstacles = set()
        self.loop = False
        for idx, x in enumerate(xs):
            print(f'Iteration: {idx+1}/{len(xs)}')
            new_matrix = copy.deepcopy(self.matrix)
            if (x[0]==starti) and (x[1]==startj):
                continue
            else:
                new_matrix[x[0]][x[1]] = '#'
                _, a = self.traverse_matrix(new_matrix, starti, startj)
                if self.loop:
                    loop_obstacles.add((x[0], x[1]))
        '''
        Here we visualize a problematic case, where the agent looked at
        -1 position that had an obstacle causing a turn and thus a loop.
        This was caused by usage of try-except. This works for having index over the list lenght,
        but not [-1] since it gives the last element.
        '''
        # Difference point=(21, 28)
        new_matrix = copy.deepcopy(self.matrix)
        new_matrix[21][28] = '#'
        _, a = self.traverse_matrix(new_matrix, starti, startj)
        
        self.visualize_grid(a)
        return len(loop_obstacles)

    def visualize_grid(self, matrix):
        '''
        This was made by ChatGPT for debugging purposes.
        '''

        # Define the size of the grid
        rows, cols = len(matrix), len(matrix[0])

        # Create a color map for the visualization
        color_map = {
            '.': 'lightgray',  # Dots
            '#': 'red',        # Hashes
            'X': 'blue'        # Path
        }

        # Create a grid for the plot
        fig, ax = plt.subplots(figsize=(cols, rows))
    
        for row in range(rows):
            for col in range(cols):
                cell = matrix[row][col]
                # Draw the grid cell with the corresponding color
                if cell in color_map:
                    ax.add_patch(plt.Rectangle((col, rows - row - 1), 1, 1, color=color_map[cell]))

        # Draw the grid lines
        for x in range(cols + 1):
            ax.axvline(x, color='black', linewidth=0.5)
        for y in range(rows + 1):
            ax.axhline(y, color='black', linewidth=0.5)
        # Set the aspect ratio to equal and remove axes
        ax.set_aspect('equal')
        ax.axis('off')
        plt.savefig("problem_plot.png", bbox_inches='tight')
        plt.show()


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
