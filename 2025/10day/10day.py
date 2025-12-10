import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time

import sys

sys.path.append("..")


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    # Function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a BFS of graph
    def BFS(self, s):
        # Mark all the vertices as not visited
        visited = [False] * (max(self.graph) + 1)

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        visited[s] = True

        while queue:
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print(s, end=" ")

            # Get all adjacent vertices of the
            # dequeued vertex s.
            # If an adjacent has not been visited,
            # then mark it visited and enqueue it
            for i in self.graph[s]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True


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

    def parse_data(self, line):
        lights = re.search(r"\[(.*?)\]", line)
        light_str = lights.group(1) if lights else ""
        light_list = [0 if char == "." else 1 for char in light_str]
        N = len(light_list)

        button_matches = re.findall(r"\((.*?)\)", line)
        buttons = []
        for match in button_matches:
            if "," in match:
                buttons.append(list(map(int, match.split(","))))
            else:
                buttons.append([int(match)])

        button_vectors = []
        for indices in buttons:
            # Create a vector of N zeros
            vector = [0] * N
            print(indices)
            # Set the positions indicated by the indices to 1 (toggle ON)
            for index in indices:
                # We need to ensure the index is valid (0 to N-1)
                if 0 <= index < N:
                    vector[index] = 1
            button_vectors.append(vector)
        buttons = button_vectors
        joltage_match = re.search(r"\{(.*?)\}", line)
        joltage_str = joltage_match.group(1) if joltage_match else ""

        joltage_list = [int(val) for val in joltage_str.split(",") if joltage_str]

        print(f"Original String: {line}\n")
        print(f"1. lights (0/1 List): {light_list}")
        print(f"2. buttons: {buttons}")
        print(f"3. joltage: {joltage_list}")
        return light_list, buttons, joltage_list

    def silver(self):
        for idx, line in enumerate(self.lines):
            light_list, buttons, joltage_list = self.parse_data(line)
            g = Graph()
            g.addEdge(light_list, buttons)
            print(g)
        return

    def gold(self):
        return


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
