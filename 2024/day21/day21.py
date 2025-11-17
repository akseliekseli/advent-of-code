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
        self.codes = [list(seq) for seq in self.lines]
        # Replace A with 10
        self.codes = [[10 if char == 'A' else int(char) for char in seq] for seq in self.codes]
    
    def num_to_coordinate(self, num):
        c1, c2 = None, None
        if num == 'A':
            return (0,2)
        elif num >0 and num<4:
            c1 = 1
        elif num >3 and num<7:
            c1 = 2
        elif num >6 and num<10:
            c1 = 3
        else: c1 = 0
        
        if num in [1, 4, 7]:
            c2 = 0
        elif num in [0, 2, 5, 8]:
            c2 = 1
        else: c2 = 2
        return (c1, c2)

    def first_steer(self, code):
        coord_n = (0, 2)
        sequence_str = ''
        for c in code:
            coord_n1 = self.num_to_coordinate(c)
            coord_diff = (coord_n1[0] - coord_n[0], coord_n1[1] - coord_n[1])
            if coord_n[0] == 0:
                if coord_diff[0] > 0: sequence_str += np.abs(coord_diff[0])*'^'
                if coord_diff[0] < 0: sequence_str += np.abs(coord_diff[0])*'v'
                if coord_diff[1] < 0: sequence_str += np.abs(coord_diff[1])*'<'
                if coord_diff[1] > 0: sequence_str += np.abs(coord_diff[1])*'>'
            else:
                if coord_diff[1] < 0: sequence_str += np.abs(coord_diff[1])*'<'
                if coord_diff[1] > 0: sequence_str += np.abs(coord_diff[1])*'>'
                if coord_diff[0] < 0: sequence_str += np.abs(coord_diff[0])*'v'
                if coord_diff[0] > 0: sequence_str += np.abs(coord_diff[0])*'^'
            sequence_str += 'A'
            coord_n = coord_n1
        return sequence_str

    def arrows_to_coords(self, arrow):
        if arrow == 'A': return (1, 2)
        elif arrow == '^': return (1,1)
        elif arrow == '<': return (0,0)
        elif arrow == 'v': return (0,1)
        elif arrow == '>': return (0,2)
        else: return None

    def robot_steers(self, seq):
        seq_robot = ''
        coord_n = (1,2)
        for s in list(seq):
            coord_n1 = self.arrows_to_coords(s)
            coord_diff = (coord_n1[0] - coord_n[0], coord_n1[1] - coord_n[1])
            if coord_n[0] == 1:
                if coord_diff[0] < 0: seq_robot += np.abs(coord_diff[0])*'v'
                if coord_diff[1] < 0: seq_robot += np.abs(coord_diff[1])*'<'
                if coord_diff[0] > 0: seq_robot += np.abs(coord_diff[0])*'^'
                if coord_diff[1] > 0: seq_robot += np.abs(coord_diff[1])*'>'
            else:
                if coord_diff[1] < 0: seq_robot += np.abs(coord_diff[1])*'<'
                if coord_diff[0] < 0: seq_robot += np.abs(coord_diff[0])*'v'
                if coord_diff[0] > 0: seq_robot += np.abs(coord_diff[0])*'^'
                if coord_diff[1] > 0: seq_robot += np.abs(coord_diff[1])*'>'
            coord_n = coord_n1
            seq_robot += 'A'
        return seq_robot


    def silver(self):
        result = 0
        for idx, code in enumerate(self.codes):
            seq = self.first_steer(code)
            seq_robot = self.robot_steers(seq)
            print(f'\n{code}: ')
            print(seq)
            print(seq_robot)
            seq_robot = self.robot_steers(seq_robot)
            print(seq_robot)
            print(len(seq_robot), int(''.join(map(str, code[:-1]))))
            result += len(seq_robot)*int(''.join(map(str, code[:-1])))
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
