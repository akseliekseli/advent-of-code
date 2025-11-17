import csv
import argparse
import numpy as np


class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()


    def first(self):
        n_safe = 0
        for item in self.lines:
            values = list(map(int, item.split()))

            diffs = np.diff(values)
            if (all(i < j for i, j in zip(values, values[1:])) or all(i > j for i, j in zip(values, values[1:]))) and np.abs(diffs).max()<4:
                n_safe = n_safe+1
        return n_safe


    def second(self):
        '''
        Tänään opittiin kaksi asiaa:
        1. Elegantin sijaan kannattaa tehdä toimiva
        2. Kuuntele kun @PauliAnt sanoo tehdävän olevan hankala ilman bruteforcea :DD
        '''

        n_safe = 0
        for item in self.lines:
            values = list(map(int, item.split()))

            diffs = np.diff(values)
            increasing, decreasing = self.check_increasing(values)
            if (increasing or decreasing) and np.abs(diffs).max()<4:
                n_safe = n_safe+1
            else:
                for ii, val in enumerate(values):
                    new = [values[jj] for jj in range(len(values)) if jj !=ii]
                    increasing, decreasing = self.check_increasing(new)
                    diffs = np.diff(new)
                    if (increasing or decreasing) and np.abs(diffs).max() < 4:
                        n_safe = n_safe + 1
                        break
                    else:
                        continue
        return n_safe

    def check_increasing(self, values):
        increasing =(all(i < j for i, j in zip(values, values[1:])))
        decreasing =(all(i > j for i, j in zip(values, values[1:])))
        return increasing, decreasing


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
