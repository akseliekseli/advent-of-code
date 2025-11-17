import csv
import argparse
import re
import numpy as np


class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()


    def first(self):
        left = []
        right = []
        for line in self.lines:
            line = line.split('   ')
            left.append(int(line[0]))
            right.append(int(line[1]))
        left.sort()
        left = np.array(left)
        right.sort()
        right = np.array(right)
        distance = np.abs(left-right)
        return np.sum(distance)

    def second(self):
        left = []
        right = []
        for line in self.lines:
            line = line.split('   ')
            left.append(int(line[0]))
            right.append(int(line[1]))
        left.sort()
        left = np.array(left)
        right.sort()
        right = np.array(right)

        similarities = np.zeros(left.shape)
        for ii, val in enumerate(left):
            similarities[ii] = val*(right == val).sum()
        return int(np.sum(similarities))



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False
    solution = Solution(test=test)
    results = solution.first() if case == 1 else solution.second()

    print(f'Results part {case}: {results}')
