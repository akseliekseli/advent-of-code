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

    def read_data(self):
        is_rules = True
        self.rules = []
        self.updates = []
        for line in self.lines:
            if line=='':
                is_rules = False
            elif is_rules:
                num1 = int(line[0]+line[1])
                num2 = int(line[3]+line[4])
                self.rules.append([num1, num2])
            else:
                self.updates.append(list(map(int, line.split(','))))
       # Create dict for the rules
        self.before_dict = {rule[0]: [] for rule in self.rules}
        for rule in self.rules: self.before_dict[rule[0]].append(rule[1]) 

    def silver(self):
        self.read_data()
        right_update = self.compute_right_updates()
        return self.compute_middle(right_update)
        
    def compute_middle(self, right_updates):
        # Compute the sum of the middle numbers
        result = 0
        for ii, update in enumerate(right_updates):
            result = result + update[len(update)//2]
        return result 

    def compute_right_updates(self):
        '''
        Check which updates are correct. Check for each point if the previous points are in its 
        ruleset. If it is, then the update is incorrect. 
        '''
        right_update = []
        correct = True
        for uu, update in enumerate(self.updates):
            for ii, page in enumerate(update):
                try:
                    if any(p in self.before_dict[page] for p in update[:ii]):
                        correct = False
                        break
                    else:
                        continue
                except:
                    continue
            if correct: right_update.append(update)
            correct = True
        return right_update 


    def gold(self):
        self.read_data()
        self.bad_updates = self.compute_bad_updates()
        bad_updates = self.fix_bad_updates()
        return self.compute_middle(bad_updates)

    def fix_bad_updates(self):
        '''
        Fixing the bad updates. Elegant solution didn't work so just loop through all the instructions.
        '''
        fixed_updates = []
        for update in self.bad_updates:
            new_update = update
            for ii in range(0, len(update)):
                for jj in range(0, len(update[ii:])):
                    try:
                        if update[ii+jj] in self.before_dict[new_update[ii]]:
                            temp = new_update[ii+jj]
                            new_update[ii+jj] = new_update[ii]
                            new_update[ii] = temp
                        else:
                            pass
                    except:
                        pass
            # Need to be flipped
            fixed_updates.append(new_update[::-1])
        return fixed_updates

    def compute_bad_updates(self):
        '''
        Computing the bad updates for the gold task. Same logic as silver task but reversed.
        '''
        bad_update = []
        bad = False
        for uu, update in enumerate(self.updates):
            for ii, page in enumerate(update):
                try:
                    if any(p in self.before_dict[page] for p in update[:ii]):
                        bad = True
                        break
                    else:
                        bad = False
                        continue
                except:
                    continue
            if bad: bad_update.append(update)
            bad = True
        return bad_update 

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()

    print(f'Results part {case}: {results}')
