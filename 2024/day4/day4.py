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
        self.char_location_mapping = {key: [] for key in ['X', 'M', 'A', 'S']}
       # Parse the input into dict with coordinates for each letter
        for ii, line in enumerate(self.lines):
            self.char_location_mapping['X'].extend(self.find_letters('X', line, ii))
            self.char_location_mapping['M'].extend(self.find_letters('M', line, ii))
            self.char_location_mapping['A'].extend(self.find_letters('A', line, ii))
            self.char_location_mapping['S'].extend(self.find_letters('S', line, ii))
        
        idx_xmas = []
        n_xmas = 0
        for x in self.char_location_mapping['X']:
            '''
            We loop through each X, find the Ms next to it and in which direction it is.
            Then we check if there are A and S if we continue same direction.
            '''
            next_positions, directions = self.find_m_positions(x)
            for ii, dir in enumerate(directions):
                pos = self.create_next_positions(next_positions[ii], dir)
                if pos in self.char_location_mapping['A']:
                    pos_s = self.create_next_positions(pos, dir)
                    if pos_s in self.char_location_mapping['S']:
                        n_xmas = n_xmas + 1
        return n_xmas

    def second(self):
        self.char_location_mapping = {key: [] for key in ['X', 'M', 'A', 'S']}
        # Parse the input into dict with coordinates for each letter
        for ii, line in enumerate(self.lines):
            self.char_location_mapping['X'].extend(self.find_letters('X', line, ii))
            self.char_location_mapping['M'].extend(self.find_letters('M', line, ii))
            self.char_location_mapping['A'].extend(self.find_letters('A', line, ii))
            self.char_location_mapping['S'].extend(self.find_letters('S', line, ii))
        
        n_xmas = 0
        for a in self.char_location_mapping['A']:
            # Window used to get the elements round letter A
            mas_window = [[a[0]-1, a[1]-1],  [a[0]+1, a[1]+1], [a[0]-1, a[1]+1], [a[0]+1, a[1]-1]]
            # Find if mas window coordinates are in M and S cell lists
            m_pos = [ii for ii, lst in enumerate(mas_window) if lst in self.char_location_mapping['M']]
            s_pos = [ii for ii, lst in enumerate(mas_window) if lst in self.char_location_mapping['S']]
            if (len(m_pos)==2) and (len(s_pos)==2) and (m_pos!=[0, 1]) and (s_pos!=[0, 1]):
                n_xmas = n_xmas + 1
        return n_xmas

    def find_letters(self, letter, input_line, idx):
        # Finding coordinates of spesific letter
        return [[idx, i] for i, ltr in enumerate(input_line) if ltr == letter]
    
    def find_m_positions(self, xs):
        '''
        Finding the M next to the given X.
        Return positions and directions
        '''
        next_possible_positions = self.create_next_positions(xs)
        next_positions = [lst for lst in next_possible_positions if lst in self.char_location_mapping['M']]
        directions = [ii for ii, lst in enumerate(next_possible_positions) if lst in self.char_location_mapping['M']]
                        
        return next_positions, directions
    
    def create_next_positions(self, x, dir=None):
        '''Window for finding next coordinates.
            dir is used to get just the desired direction.
        '''
        positions = []
        positions.append([x[0], x[1]+1])
        positions.append([x[0]+1, x[1]+1])
        positions.append([x[0]+1, x[1]])
        positions.append([x[0]-1, x[1]+1])
        positions.append([x[0]-1, x[1]])
        positions.append([x[0]-1, x[1]-1])
        positions.append([x[0], x[1]-1])
        positions.append([x[0]+1, x[1]-1])
        if dir != None:
            positions = positions[dir]
        return positions


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
