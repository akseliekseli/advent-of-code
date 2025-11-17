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
        self.addition = lambda a, b: a + b
        self.multiplication = lambda a, b: a * b

    def first(self):
        calibration_result = 0
        for line in self.lines:
            cols = line.split(':')
            target = int(cols[0])
            nums = [int(num) for num in cols[1].lstrip().split(' ')]
            if self.recursive_operations(target, nums):
                calibration_result += target
        return calibration_result

    def recursive_operations(self, target, operations):
        if len(operations)==1:
            return operations[0] == target
        for operator in self.operators:
            new = [operator(operations[0], operations[1])]
            new_list = new + operations[2:]
            if self.recursive_operations(target, new_list):
                return True
        return False

    '''
    This was my first try to go backwards.
    It would reduce the computation costs, because you can see, that if the last
    operation is not a factor of the target, the operator has to be sum.
    '''
    def evaluate_backwards_operations(self, target, operations):
        print(f'\nTARGET: {target}') 
        for ii, operation in enumerate(operations[::-1]):
            if (target) % operation != 0:
                target -= operation
                print(f'+ {operation}')
            else:
                target /= operation
                print(f'* {operation}')
        if target == 1: return True
        else: return 0

    def second(self):
        self.concatenate = lambda a, b: int(str(a) + str(b))
        self.operators = [self.addition, self.multiplication, self.concatenate]
        return self.first()

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
