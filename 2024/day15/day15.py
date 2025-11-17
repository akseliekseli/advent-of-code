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
        
        self.boxes = []
        self.robot = ()
        self.instructions = ''
        for ii, line in enumerate(self.lines):
            if line == '':
                pass
            elif line[0] == "#":
                self.boxes.append([])
                for jj, char in enumerate(line):
                    self.boxes[ii].append(char)
                    if line[jj] == '@':
                        self.robot = (ii, jj)
                print(line)
            else:
                self.instructions = self.instructions + line
        self.rows = len(self.boxes)
        self.cols = len(self.boxes[0])

    def gold_data(self):
        self.boxes = []
        self.robot = ()
        self.instructions = ''
        for ii, line in enumerate(self.lines):
            if line == '':
                pass
            elif line[0] == "#":
                self.boxes.append([])
                for jj, char in enumerate(line):
                    if char=='#':
                        self.boxes[ii].append('#')
                        self.boxes[ii].append('#')
                    if char=='O':
                        self.boxes[ii].append('[')
                        self.boxes[ii].append(']')
                    if char=='.':
                        self.boxes[ii].append('.')
                        self.boxes[ii].append('.')
                    if char=='@':
                        self.robot = (ii, jj)
                        self.boxes[ii].append('@')
                        self.boxes[ii].append('.') 
                print(self.boxes[ii])
            else:
                self.instructions = self.instructions + line
        self.rows = len(self.boxes)
        self.cols = len(self.boxes[0])

    def move_up(self):
        col = []
        for ii in range(self.robot[0], -1, -1):
            col.append(self.boxes[ii][self.robot[1]])
        try: first_dot = col.index('.')
        except: first_dot = -1
        try: first_cross = col.index('#')
        except: first_dot = -1
        if first_dot == -1: pass
        elif first_cross < first_dot: pass
        elif first_dot == 1:
            self.boxes[self.robot[0]-1][self.robot[1]] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0]-1, self.robot[1])
        else:
            self.boxes[self.robot[0]-1][self.robot[1]] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.boxes[self.robot[0]-first_dot][self.robot[1]] = 'O'
            self.robot = (self.robot[0]-1, self.robot[1])

    def move_right(self):
        col = []
        for ii in range(self.robot[1], self.cols):
            col.append(self.boxes[self.robot[0]][ii])
        try: first_dot = col.index('.')
        except: first_dot = -1
        try: first_cross = col.index('#')
        except: first_dot = -1
        if first_dot == -1: pass
        elif first_cross < first_dot: pass
        elif first_dot == 1:
            self.boxes[self.robot[0]][self.robot[1]+1] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0], self.robot[1]+1)
        else:
            self.boxes[self.robot[0]][self.robot[1]+1] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.boxes[self.robot[0]][self.robot[1]+first_dot] = 'O'
            self.robot = (self.robot[0], self.robot[1]+1)
    
    def move_down(self):
        col = []
        for ii in range(self.robot[0], self.rows):
            col.append(self.boxes[ii][self.robot[1]])
        try: first_dot = col.index('.')
        except: first_dot = -1
        try: first_cross = col.index('#')
        except: first_dot = -1
        if first_dot == -1: pass
        elif first_cross < first_dot: pass
        elif first_dot == 1:
            self.boxes[self.robot[0]+1][self.robot[1]] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0]+1, self.robot[1])
        else:
            self.boxes[self.robot[0]+1][self.robot[1]] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.boxes[self.robot[0]+first_dot][self.robot[1]] = 'O'
            self.robot = (self.robot[0]+1, self.robot[1])
    
    def move_left(self):
        col = []
        for ii in range(self.robot[1], -1, -1):
            col.append(self.boxes[self.robot[0]][ii])
        try: first_dot = col.index('.')
        except: first_dot = -1
        try: first_cross = col.index('#')
        except: first_dot = -1
        if first_dot == -1: pass
        elif first_cross < first_dot: pass
        elif first_dot == 1:
            self.boxes[self.robot[0]][self.robot[1]-1] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0], self.robot[1]-1)
        else:
            self.boxes[self.robot[0]][self.robot[1]-1] = '@'
            self.boxes[self.robot[0]][self.robot[1]] = '.'
            self.boxes[self.robot[0]][self.robot[1]-first_dot] = 'O'
            self.robot = (self.robot[0], self.robot[1]-1)

    def silver(self):
        for instruction in self.instructions:
            if instruction == '^': self.move_up()
            elif instruction == '>': self.move_right()
            elif instruction == 'v': self.move_down()
            elif instruction == '<': self.move_left()
            for line in self.boxes:
                print(line)
            print('\n')
        result = 0
        for ii in range(0, self.rows):
            for jj in range(0, self.cols):
                if self.boxes[ii][jj] == 'O':
                    result += 100*ii + jj
        return result


    def gold(self):
        self.gold_data()
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
