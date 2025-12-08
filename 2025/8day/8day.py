import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import math


class Solution:
    input_filename = "input.txt"
    input_filename_test = "example.txt"

    def __init__(self, test=False):
        self.file = (
            open(self.input_filename_test, "r").read()
            if test
            else open(self.input_filename, "r").read()
        )
        self.lines = self.file.splitlines()
        self.test = test

    def silver(self):
        """
        1. Compute distances
        2. Create a list where each circuit is represented as a set
        3. Loop through the shortest distances, merge sets and remove the sets
        that have been merged.
        """
        boxes = defaultdict(int)
        for ii, box in enumerate(self.lines):
            boxes[ii] = [int(x) for x in box.split(",")]
        print(boxes)
        distances_dict = defaultdict(float)
        for key1 in boxes.keys():
            for key2 in boxes.keys():
                if key1 == key2:
                    continue
                a1, a2, a3 = boxes[key1]
                b1, b2, b3 = boxes[key2]
                dist = math.sqrt((b1 - a1) ** 2 + (b2 - a2) ** 2 + (b3 - a3) ** 2)
                distances_dict[dist] = [key1, key2]

        dists = sorted(list(distances_dict.keys()))
        circuits = []
        for ii in boxes.keys():
            circuits.append({ii})

        if self.test:
            n_iter = 10
        else:
            n_iter = 1000

        for ii in range(0, n_iter):
            d = dists[ii]
            shortest_points = distances_dict[d]
            merged_set = set(shortest_points)
            circuits_to_remove = []
            for circuit in circuits:
                if any(p in circuit for p in shortest_points):
                    merged_set = merged_set.union(circuit)
                    circuits_to_remove.append(circuit)
            if circuits_to_remove:
                for circuit in circuits_to_remove:
                    circuits.remove(circuit)
                circuits.append(merged_set)
        return math.prod(sorted([len(x) for x in circuits])[-3:])

    def gold(self):
        """
        Same idea as in silver, but changed to while loop that check when
        the size of the smallest circuit is > 1.
        """
        boxes = defaultdict(int)
        for ii, box in enumerate(self.lines):
            boxes[ii] = [int(x) for x in box.split(",")]
        print(boxes)
        distances_dict = defaultdict(float)
        for key1 in boxes.keys():
            for key2 in boxes.keys():
                if key1 == key2:
                    continue
                a1, a2, a3 = boxes[key1]
                b1, b2, b3 = boxes[key2]
                dist = math.sqrt((b1 - a1) ** 2 + (b2 - a2) ** 2 + (b3 - a3) ** 2)
                distances_dict[dist] = [key1, key2]

        dists = sorted(list(distances_dict.keys()))
        circuits = []
        for ii in boxes.keys():
            circuits.append({ii})

        ii = 0
        while True:
            d = dists[ii]
            shortest_points = distances_dict[d]
            merged_set = set(shortest_points)
            circuits_to_remove = []
            for circuit in circuits:
                if any(p in circuit for p in shortest_points):
                    merged_set = merged_set.union(circuit)
                    circuits_to_remove.append(circuit)
            if circuits_to_remove:
                for circuit in circuits_to_remove:
                    circuits.remove(circuit)
                circuits.append(merged_set)
            min_len_circuit = sorted([len(x) for x in circuits])[0]
            if min_len_circuit > 1:
                break
            ii += 1

        a, b = shortest_points
        return boxes[a][0] * boxes[b][0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="True/False")
    parser.add_argument("-c", help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.c)
    test = True if args.t in ["True", "true"] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()
    end = time.time()
    print(f"Results part {case}: {results}")
    print(f"Runtime: {end - start}")
