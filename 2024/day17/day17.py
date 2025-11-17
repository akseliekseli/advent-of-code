import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time

'''
Pen and paper + lots of prints and trial and error to get on track
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        
        self.A = int(self.lines[0].split()[2])
        self.B = int(self.lines[1].split()[2])
        self.C = int(self.lines[2].split()[2])
        program = self.lines[4].split()[1].split(',')
        self.program = list(map(int, program))
        self.instructions = [self.adv,
                             self.bxl,
                             self.bst,
                             self.jnz,
                             self.bxc,
                             self.out,
                             self.bdv,
                             self.cdv]

    def get_combo(self, literal):
        if literal < 4: return literal
        elif literal == 4: return self.A
        elif literal == 5: return self.B
        elif literal == 6: return self.C
        elif literal == 7: pass
    
    def adv(self, literal):
        combo = self.get_combo(literal)
        self.A = int(self.A // 2**combo)
        return True

    def bxl(self, literal):
        self.B = self.B ^ literal
        return True

    def bst(self, literal):
        combo = self.get_combo(literal)
        self.B = combo % 8
        return True

    def jnz(self, literal):
        if self.A == 0: return True
        else: return False

    def bxc(self, literal):
        self.B = self.B ^ self.C
        return True

    def out(self, literal):
        combo = self.get_combo(literal)
        self.output.append(combo%8)
        return True

    def bdv(self, literal):
        combo = self.get_combo(literal)
        self.B = int(self.A // 2**combo)
        return True

    def cdv(self, literal):
        combo = self.get_combo(literal)
        self.C = int(self.A // 2**combo)
        return True

    def silver(self):
        self.output = []
        pointer = 0
        while pointer != len(self.program):
            ii = self.program[pointer]
            instruction = self.instructions[ii]
            literal = self.program[pointer+1]
            if not instruction(literal):
                pointer = literal
            else:
                pointer += 2
        result = ",".join(map(str, self.output))
        return result

    def run_instructions(self):
        '''
        This was used for initial investigation of the algorithm
        '''
        pointer = 0
        while pointer != len(self.program):
            ii = self.program[pointer]
            instruction = self.instructions[ii]
            literal = self.program[pointer+1]
            if not instruction(literal):
                pointer = literal
            else:
                pointer += 2
            print(f'ii: {ii}, literal: {literal}, output: {self.output}')
            print(self.A, self.B, self.C)

        result = ",".join(map(str, self.output))
        print(f'{result}\n')
        return result
        
    def input_loop(self, A):
        B = A%8
        B = B ^ 5
        C = A//2**B
        B = B^6
        A = A//2**3
        B = B ^ C
        out = B % 8
        return out
         
    def recursion_find_a(self, A, idx):
        output = self.input_loop(A)
        if output != self.program[idx]:
            return 
        if idx == 0:
            self.A_list.append(A)
        else:
            for a_next in range(0, 8):
                self.recursion_find_a(A*8 + a_next, idx-1)

    def gold(self):
        print(self.program)
        self.output = []
        '''
        First I examined the outputs with different A
        -> Found that it has a pattern
        -> Did deeper analysis on the input algorithm

        -> Tried simple while loop for solving the A, but needed
            to switch to recursive search

        (2,4): A <- B%8
        (1,5): B <- B^5
        (7,5): C <- A/2**B
        (1,6): B <- B^6
        (0,3): A <- A/2**3
        (4,2): B <- B^C
        (5,5): out = B%8
        (3,0): repeat from top
        '''
        self.A_list = []
        input_idx = len(self.program)-1
        for a in range(0, 8):
            self.recursion_find_a(a, input_idx)
        A = self.A_list[0]
        '''
        First Try.
        This didn't work, since at the middle of the sequence
        the bits change due to having more instructions having
        too low or large numbers (overlapping multiplies of ten)

        Needed to do with recursion to check all the bits

        while input_idx >= 0:
            output = self.input_loop(A)
            print(output)
            if output != self.program[input_idx]:
                print(output)
                A += 1
            else:
                print("HEREEE")
                A = A*8
                input_idx -= 1
                outputs.append(output)
        print(A)
        print(outputs[::-1])
        print(self.program)
        '''
        
        self.A = A
        self.B = 0
        self.C = 0
        print(self.silver())
        return A


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
