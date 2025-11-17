import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time


'''
Matrix stuff <3

Had a bug because int(coeffs[1]) transforms for example 86.9999 to 86 instead of 87.
I knew this, but was just dumb not to think about it earlier :DDD
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.instructions = defaultdict(list)
        key = 0
        for line in self.lines:
            if line == '':
                key += 1
            else:
                numbers = re.findall(r'\d+', line)
                self.instructions[key].append((int(numbers[0]), int(numbers[1])))

    def calculate_linear_combination_and_tokens(self, padding=0):
        n_tokens = 0
        for i in self.instructions.keys():
            instruction = self.instructions[i]
            u = np.array(instruction[0])
            w = np.array(instruction[1])
            # Padding added for the gold task
            v = np.array(instruction[2])+padding
            A = np.column_stack((u, w))
            try:
                # Finding a linear combination of the two vectors
                coeffs = np.linalg.solve(A, v)
                # The padding is added for the gold task
                if round(coeffs[0], 3).is_integer() and round(coeffs[1], 3).is_integer() and coeffs[0] <= (100+padding) and coeffs[1] <= (100+padding):
                    n_tokens += int(round(coeffs[0])*3) + int(round(coeffs[1]))
            except np.linalg.LinAlgError:
                '''
                Here we just check which button to press if the two buttons are a linear combination of each other.
                '''
                if  instruction[2][1] % instruction[0][1]== 0 and instruction[2][1] % instruction[1][1]== 0:
                    if instruction[2][1] / instruction[0][1] < 3*(instruction[2][1] / instruction[1][1]):
                        n_tokens += 3*(instruction[2][0] // instruction[0][0])
                    else:
                        n_tokens += (instruction[2][1] // instruction[1][1])
                if instruction[2][1] % instruction[1][1]== 0:
                    n_tokens += (instruction[2][1] // instruction[1][1])
                elif instruction[2][0] % instruction[0][0]== 0:
                    n_tokens += 3*(instruction[2][0] // instruction[0][0])
        return n_tokens


    def silver(self):
        return self.calculate_linear_combination_and_tokens()

    def gold(self):
        return self.calculate_linear_combination_and_tokens(10000000000000)


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
