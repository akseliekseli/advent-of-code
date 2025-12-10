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

    def get_coords(self):
        coords = []
        self.coords = set()
        for ii, line in enumerate(self.lines):
            coords.append([int(a) for a in line.split(",")])
            self.coords.add((int(line.split(",")[0]), int(line.split(",")[1])))
        return coords

    def silver(self):
        coords = self.get_coords()

        area_largest = 0
        for ii in range(0, len(coords)):
            for jj in range(0, len(coords)):
                a = abs(coords[ii][0] - coords[jj][0]) + 1
                b = abs(coords[ii][1] - coords[jj][1]) + 1
                area = a * b
                if area > area_largest:
                    area_largest = area

        return area_largest

    def scanline_fill(self, polygon, height, width):
        canvas = [[0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            intersections = []
            for i in range(len(polygon)):
                x1, y1 = polygon[i]
                x2, y2 = polygon[(i + 1) % len(polygon)]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if y1 != y2:
                        x_intersect = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                        intersections.append(x_intersect)
            intersections.sort()
            for i in range(0, len(intersections), 2):
                start = int(intersections[i])
                end = int(intersections[i + 1]) if i + 1 < len(intersections) else width
                for x in range(start, end):
                    if 0 <= x < width:
                        canvas[y][x] = 1
        return canvas

    def largest_rectangle_area(self, heights):
        stack = [-1]
        heights.append(0)
        max_area = 0
        candidates = []
        for i in range(len(heights)):
            while heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                current_area = h * w
                start_col = stack[-1] + 1

                candidates.append((current_area, h, w, start_col))
            stack.append(i)
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates

    def maximal_rectangle(self, matrix):
        if not matrix or not matrix[0]:
            return 0

        n = len(matrix[0])
        heights = [0] * n
        max_area = 0
        for ii, row in enumerate(matrix):
            points = set()
            for i in range(n):
                points.add((ii, i))
                if row[i] == 1:
                    heights[i] += 1
                else:
                    heights[i] = 0
            candidates = self.largest_rectangle_area(heights)
            for cand in candidates:
                current_area, h, w, start_col = cand
                corners = {(start_col, ii), (start_col + w - 1, ii - h + 1)}
                corners2 = {
                    (start_col, ii - h + 1),
                    (start_col + w - 1, ii),
                }
                if not corners.issubset(self.polygon_points) and not corners2.issubset(
                    self.polygon_points
                ):
                    continue
                if (
                    len(corners.intersection(self.coords)) >= 2
                    or len(corners2.intersection(self.coords)) >= 2
                ):
                    max_area = max(max_area, current_area)
        return max_area

    def gold(self):
        coords = self.get_coords()
        print(coords)
        max_coords = max(max([c for c in coords]))
        canvas = self.scanline_fill(coords, max_coords, max_coords)
        print("canva done")

        self.polygon_points = set()
        ii = 1
        self.polygon_points.add((coords[0][0], coords[0][1]))
        dir = self.rotate_dir(coords[0], coords[1])
        next = coords[0]
        while ii < len(coords):
            next = [next[0] + dir[0], next[1] + dir[1]]
            self.polygon_points.add((next[0], next[1]))
            if next == coords[ii]:
                if ii == len(coords) - 1:
                    dir = self.rotate_dir(coords[ii], coords[0])
                else:
                    dir = self.rotate_dir(coords[ii], coords[ii + 1])
                ii += 1
        while next != coords[0]:
            next = [next[0] + dir[0], next[1] + dir[1]]
            self.polygon_points.add((next[0], next[1]))
        print("polygon_ppints done")
        for ii, canva in enumerate(canvas):
            for jj, point in enumerate(canva):
                if point == 1:
                    self.polygon_points.add((jj, ii))
        print("canva done")
        area_largest = 0

        grid = []
        for ii in range(0, max_coords + 1):
            line = [0 for i in range(0, max_coords + 1)]
            for jj in range(0, max_coords + 1):
                if (jj, ii) in self.polygon_points:
                    line[jj] = 1
            grid.append(line)
            print(line)

        return self.maximal_rectangle(grid)

    def rotate_dir(self, p_current, p_next):
        delta_x = p_next[0] - p_current[0]
        delta_y = p_next[1] - p_current[1]
        if delta_x == 0:
            dx = 0
        else:
            dx = int(math.copysign(1, delta_x))
        if delta_y == 0:
            dy = 0
        else:
            dy = int(math.copysign(1, delta_y))
        return [dx, dy]


"""
1381179345 too low
2701846272 not right
2927930377

"""

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
