import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict, Counter
import time

'''
Thanks @PauliAnt for help in finding the bug in the gold task. 

Should read the instructions more carefully :DD
'''    

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.numbers = []
        for ii, num in enumerate(self.lines):
            self.numbers.append(int(num))
    
    def secret(self, num):
        next = ((num * 64) ^ num)% 16777216
        next = (int(next // 32) ^ next) % 16777216 
        next = ((next*2048) ^ next) % 16777216
        return next

    def silver(self):
        result = 0
        self.N_ITER = 2000
        for num in self.numbers:
            for ii in range(0, self.N_ITER):
                num = self.secret(num)
            result += num
        return result

    def gold(self):
        self.N_ITER = 2000
        self.secrets = defaultdict(list)
        self.sequences_counter = Counter()

        for num in self.numbers:
            n = num
            prev = None
            diffs = []
            for ii in range(0, self.N_ITER):
                n = self.secret(n)
                self.secrets[num].append(n)
                if ii == 0:
                    diffs.append(None)
                    prev = n%10
                else:
                    last_digit = n % 10
                    diffs.append(last_digit - prev)
                    prev = last_digit
            seen_sequences = set()
            for ii in range(4, self.N_ITER):
                secrets_sequence = (diffs[ii-3], diffs[ii-2], diffs[ii-1], diffs[ii])
                if secrets_sequence not in seen_sequences:
                    seen_sequences.add(secrets_sequence)
                    self.sequences_counter[secrets_sequence] += self.secrets[num][ii] % 10

            
        return self.sequences_counter.most_common()[0]
        

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
