import csv
import argparse
import re
import numpy as np
import time

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()


    def first(self):
        line = self.lines[0]
        output = []
        next_number = 0
        for idx, num in enumerate(line):
            if idx % 2 == 0:
                output.extend(int(num)*[next_number])
                next_number += 1
            else:
                output.extend(int(num)* ['.'])        
        ii = 0
        checksum = 0
        # Loop throught the input and replace the dots
        while ii < len(output):
            if output[ii] == '.':
                output[ii] =output[-1]
                output.pop(-1)
            else:
                ii += 1
        assert '.' not in output
        for ii in range(0, len(output)):
            checksum += ii*int(output[ii])
        return checksum 


    def second(self):
        line = self.lines[0]
        output = []
        next_number = 0
        for idx, num in enumerate(line):
            if idx % 2 == 0:
                output.extend(int(num)*[next_number])
                next_number += 1
            else:
                output.extend(int(num)* ['.'])       
        '''
        Create tuples for dot and number sequences
        dot: (start_idx, length)
        number: (start_idx, length, value)
        '''
        dots = self.find_dots_sequences(output)
        numbers = self.find_number_sequences(output)
        len_output = len(output) 
        for ii, num in enumerate(numbers[::-1]):
            if num[2] != '.':
                for jj, dot in enumerate(dots):
                    if num[1] <= dot[1] and dot[0] < num[0]:
                        output[dot[0]:dot[0]+num[1]] = [num[2]]*num[1]
                        output[num[0]:num[0]+num[1]] = ['.']*num[1]
                        # Change the tuple of the dot or pop if it is full
                        if num[1] < dot[1]:
                            dots[jj] = (dot[0]+num[1], dot[1]-num[1])
                        else:
                            dots.pop(jj)
                        break
                
        assert len(output) == len_output
        
        checksum = 0
        for ii in range(0, len(output)):
            if output[ii] != '.':
                checksum += ii*int(output[ii])
        return checksum

    def find_number_sequences(self, lst):
        sequences = []
        i = 0
        n = len(lst)

        while i < n:
            current = lst[i]
            start = i
            count = 0
            while i < n and lst[i] == current:
                count += 1
                i += 1
            if count >= 1:
                sequences.append((start, count, current))
        return sequences

    def find_dots_sequences(self, lst):
        sequences = []
        i = 0
        n = len(lst)
        while i < n:
            if lst[i] == '.':
                start = i
                count = 0
                while i < n and lst[i] == '.':
                    count += 1
                    i += 1
                sequences.append((start, count))
            else:
                i += 1
        return sequences


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
