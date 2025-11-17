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
    blinks = 25

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()


    def first(self):
        '''
        We utilize defaultdict with:
        keys: stone values
        values: number of stone with said value

        Dict is much faster than a Python list, so thats why the solution was
        transformed to use that.
        '''
        stones_list = self.lines[0].split()
        stones = defaultdict(int)
        for ii, stone in enumerate(stones_list):
            stones[int(stone)] = 1
        
        for jj in range(0, self.blinks):
            stones_new = defaultdict(int)
            for stone, ii in stones.items():
                ''' ii is the number of spesific stones
                 While looping through list, we add the ii to stones_new,
                because there are multiple ways to get the same stone value
                    '''
                if stone == 0:
                    stones_new[1] += ii
                elif len(str(stone)) % 2 == 0:
                    n_nums = len(str(stone))//2
                    key_1 = int(str(stone)[:n_nums])
                    key_2 = int(str(stone)[n_nums:])
                    stones_new[key_1] += ii
                    stones_new[key_2] += ii
                else:
                    stones_new[stone*2024] = ii
            stones = stones_new
            #print(f'blink {jj+1}: {stones}')
        return sum(stones.values())
    
    def second(self):
        self.blinks = 75
        return self.first()


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
