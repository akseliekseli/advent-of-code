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
        result = 0
        for line in self.lines:
            x = re.findall(r"mul\(([0-9]+,[0-9]+)\)", line)
            for item in x:
                items = item.split(",")
                result = result + int(items[0])*int(items[1])

        return result

    def second(self):
        result = 0
        do = True
        for line in self.lines:
            # Aika purkka regex, antaa [mul(2,4), '2,4'] tai ['do()/don't(), '']
            # Toimii kuitenki
            x = re.findall(r"(mul\(([0-9]+,[0-9]+)\)|do\(\)|don't\(\))", line)
            for item in x:
                items = list(item)
                if items[0] == "don't()":
                    do = False
                elif items[0] == "do()":
                    do = True
                if do:
                    numbers = items[1].split(',')
                    if len(numbers)==2:
                        result = result + int(numbers[0])*int(numbers[1])
        return result


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
