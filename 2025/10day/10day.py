import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
from collections import deque
from itertools import combinations
from scipy.optimize import linprog
import sys

sys.path.append("..")


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
        """
        Parsing the data. This took quite long to code.
        Helpful website to test regex: https://regex101.com/
        """
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

        # one-hot encode buttons
        button_vectors = []
        for indices in buttons:
            vector = [0] * N
            for index in indices:
                if 0 <= index < N:
                    vector[index] = 1
            button_vectors.append(vector)
        buttons = button_vectors

        joltage_match = re.search(r"\{(.*?)\}", line)
        joltage_str = joltage_match.group(1) if joltage_match else ""
        joltage_list = [int(val) for val in joltage_str.split(",") if joltage_str]

        return light_list, buttons, joltage_list

    def silver(self):
        """
        Try all the button combinations starting from the shortest.
        First to transform all off vector to desired is the shortest combo.
        """
        n_button_presses = 0
        for idx, line in enumerate(self.lines):
            light_list, buttons, joltage_list = self.parse_data(line)

            all_button_combinations = []
            for k in range(1, len(buttons) + 1):
                combinations_of_length_k = list(combinations(range(len(buttons)), k))
                all_button_combinations.extend(combinations_of_length_k)
            for combo in all_button_combinations:
                res_vector = np.zeros(len(light_list), dtype=int).T
                for btn_idx in combo:
                    # XOR to apply the button
                    res_vector = res_vector ^ np.array(buttons[btn_idx])
                if (res_vector == np.array(light_list)).all():
                    n_button_presses += len(combo)
                    break
        return n_button_presses

    def gold(self):
        """
        Linear optimization as the legendary Sirkku taught us in a Bsc course. :D
        """
        n_button_presses = 0
        for idx, line in enumerate(self.lines):
            light_list, buttons, joltage_list = self.parse_data(line)

            c = np.ones(len(buttons))
            A_eq = np.array(buttons).T
            b_eq = np.array(joltage_list)
            # print(A_eq)
            # print(c)
            # print(b_eq)
            # integrality=1 to have integer variables
            result = linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=1)
            n_button_presses += result.fun
        return int(n_button_presses)


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
