import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time

'''
Silver task: Simple search of the graph
Gold task: Bron-Kerbosch algorithm (https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm)
            for finding all the cliques and then taking the longest one.
'''

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.graph = defaultdict(set)
        for line in self.lines:
            a, b = line.split('-')
            self.graph[a].add(b)
            self.graph[b].add(a)

    def silver(self):
        # Just loop all nodes starting with t and check
        # if the connections loop
        self.cliques_3 = set()
        for key in self.graph.keys():
            if key[0] == 't':
                for conn in self.graph[key]:
                    for conn2 in self.graph[conn]:
                        if key in self.graph[conn2]:
                            self.cliques_3.add(tuple(sorted((key, conn, conn2))))
        return len(self.cliques_3)
    
    def bron_kerbosch(self, R, P, X):
        # Implemented the algorithm from pseudocode.
        if not P and not X:
            self.cliques.append(",".join(map(str, sorted(R))))
            return 
        for v in list(P): # Making P a list to allow modifications in loop
            self.bron_kerbosch(
                R.union({v}),
                P.intersection(self.graph[v]),
                X.intersection(self.graph[v])
            )
            P.remove(v)
            X.add(v)
                    
    def gold(self):
        self.cliques = []
        self.bron_kerbosch(set(), set(self.graph.keys()), set())
        largest_clique = max(self.cliques, key=len)
        return largest_clique


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
