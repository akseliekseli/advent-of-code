import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import math

"""
Reference: https://stackoverflow.com/questions/5931735/finding-largest-rectangle-in-2d-array
"""


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

    def gold2(self):
        coords = self.get_coords()

        area_largest = 0
        areas = []
        for ii in range(0, len(coords)):
            for jj in range(0, len(coords)):
                a = abs(coords[ii][0] - coords[jj][0]) + 1
                b = abs(coords[ii][1] - coords[jj][1]) + 1
                area = a * b
                areas.append((area, coords[ii], coords[jj]))
                if area > area_largest:
                    area_largest = area
        areas.sort(key=lambda x: x[0], reverse=True)
        for area in areas:
            opposite_corners = [(area[2][0], area[1][1]), (area[1][0], area[2][1])]

            print(area, opposite_corners)

        return areas[0]

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
                for x in range(start, end + 1):
                    if 0 <= x < width:
                        canvas[y][x] = 1
        return canvas

    def gold(self):
        self.reds = defaultdict(list)
        for ii, line in enumerate(self.lines):
            a, b = line.split(",")
            self.reds[int(b)].append(int(a))
        max_row = max(a for a in self.reds.keys())
        min_row = min(a for a in self.reds.keys())
        max_col = max(max(a for a in self.reds.values()))
        self.active_rectangles = []
        self.passive_rectangles = []

        # NOTE: (col, row, height, width)

        for jj in range(0, len(self.reds[min_row]), 2):
            self.add_new_active(min_row, jj)

        print(self.active_rectangles)
        for row in range(min_row + 1, max_row + 1):
            if self.reds[row] == []:
                for ii in range(0, len(self.active_rectangles)):
                    self.active_rectangles[ii] = self.increment_active(
                        self.active_rectangles[ii]
                    )
                continue
            print(self.reds[row])
            self.active_rectangles = sorted(self.active_rectangles)
            for jj in range(0, len(self.reds[row]), 2):
                end, start = self.reds[row][jj + 1], self.reds[row][jj]
                new_recs = []
                ii_pop = []
                for ii, rec in enumerate(self.active_rectangles):
                    # PERF: Space for existing to grow
                    if start <= rec[0] and end >= rec[0] + rec[3]:
                        self.active_rectangles[ii] = self.increment_active(rec)
                    # TODO: Obstacles
                    elif start < rec[0] and end < rec[0] + rec[3]:
                        ii_pop.append(ii)
                        self.passive_rectangles.append(rec)
                        a, b = self.split_active_left(rec, start, end)
                        new_recs.append(a)
                        new_recs.append(b)
                    elif start > rec[0] and end < rec[0] + rec[3]:
                        ii_pop.append(ii)
                        self.passive_rectangles.append(rec)
                        self.split_active_right(rec, start, end)
                        a, b = self.split_active_left(rec, start, end)
                        new_recs.append(a)
                        new_recs.append(b)

                self.active_rectangles = [
                    i for j, i in enumerate(self.active_rectangles) if j not in ii_pop
                ]
                for rec in new_recs:
                    print(rec)
                    self.active_rectangles.append(rec)
                print(self.active_rectangles)
                # TODO: Obstacles that require removal from active_rectangles
                self.add_new_active(row, jj)

        return

    def split_active_left(self, rec, start, end):
        return (rec[0], rec[1], rec[2], end - rec[0]), (
            end,
            rec[1],
            rec[2],
            rec[3] - end,
        )

    def split_active_right(self, rec, start, end):
        return (rec[0], rec[1], rec[2], start - rec[0]), (
            start,
            rec[1],
            rec[2],
            rec[3] - end,
        )

    def add_new_active(self, row, jj):
        # NOTE: (col, row, height, width)
        self.active_rectangles.append(
            (
                self.reds[row][jj],
                row,
                1,
                self.reds[row][jj + 1] - self.reds[row][jj],
            )
        )

    def increment_active(self, rectangle):
        return (rectangle[0], rectangle[1], rectangle[2] + 1, rectangle[3])

    def gold3(self):
        coords = self.get_coords()
        max_coords = max(max([c for c in coords]))
        # canvas = self.scanline_fill(coords, max_coords, max_coords)

        self.polygon_points = defaultdict(list)
        self.polygon_points_rows = defaultdict(list)
        self.target_corners = []
        ii = 1
        self.polygon_points[coords[0][0]].append(coords[0][1])
        self.polygon_points_rows[coords[0][1]].append(coords[0][0])
        dir = self.rotate_dir(coords[0], coords[1])
        next = coords[0]
        target = [0, -1]
        while ii < len(coords):
            next = [next[0] + dir[0], next[1] + dir[1]]
            self.polygon_points[next[0]].append(next[1])
            self.polygon_points_rows[next[1]].append(next[0])
            if next == coords[ii]:
                if ii == len(coords) - 1:
                    dir = self.rotate_dir(coords[ii], coords[0])
                else:
                    dir = self.rotate_dir(coords[ii], coords[ii + 1])
                ii += 1
        while next != coords[0]:
            next = [next[0] + dir[0], next[1] + dir[1]]
            self.polygon_points[next[0]].append(next[1])
            self.polygon_points_rows[next[1]].append(next[0])

        sorted_keys = sorted(
            self.polygon_points_rows,
            key=lambda k: len(self.polygon_points_rows[k]),
            reverse=True,
        )
        two_longest_keys = sorted_keys[:2]
        print(two_longest_keys)

        for key in two_longest_keys:
            cols = sorted(self.polygon_points_rows[key])
            for ii in range(0, len(cols)):
                if cols[ii + 1] > cols[ii] + 1:
                    self.target_corners.append([cols[ii], int(key)])
                    break
        print(self.target_corners)

        import matplotlib.pyplot as plt
        import numpy as np

        x = []
        y = []
        for key in self.polygon_points.keys():
            for point in self.polygon_points[key]:
                x.append(int(key))
                y.append(int(point))
        x = np.array(x)
        y = np.array(y)
        aas, bbs = [], []
        corners_x = []
        corners_y = []
        areas = []
        r = []
        co = []
        for idx, point in enumerate(self.target_corners):
            col, row = point
            print(col, row)
            corners_x.append(col)
            corners_y.append(row)
            if idx == 0:
                for ii in range(row, len(self.polygon_points_rows)):
                    row_points = self.polygon_points_rows[ii]
                    for p in row_points:
                        r.append(ii)
                        co.append(p)
                        ma = max(self.polygon_points[col])
                        mi = min(self.polygon_points[col])
                        if [p, ii] in coords and (mi <= ii <= ma):
                            aas.append(ii)
                            bbs.append(p)
                            area = (abs(row - ii) + 1) * (abs(col - p) + 1)
                            areas.append((area, (p, ii)))
            elif idx == 1:
                for ii in range(row, 0, -1):
                    row_points = self.polygon_points_rows[ii]
                    for p in row_points:
                        ma = max(self.polygon_points[col])
                        mi = min(self.polygon_points[col])
                        if [p, ii] in coords and (mi <= ii <= ma):
                            aas.append(ii)
                            bbs.append(p)
                            area = (abs(row - ii) + 1) * (abs(col - p) + 1)
                            areas.append((area, (p, ii)))
        sorted_areas = sorted(areas, key=lambda item: item[0], reverse=True)
        print(sorted_areas[0])

        plt.scatter(x, y, s=1)
        plt.scatter(np.array(co), np.array(r), s=1)
        plt.scatter(
            np.array([sorted_areas[0][1][0]]), np.array([sorted_areas[0][1][1]])
        )
        plt.scatter(np.array(corners_x[0]), np.array(corners_y[0]))
        # plt.show()
        return sorted_areas[0][0]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="True/False")
    parser.add_argument("-c", help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.c)
    test = True if args.t in ["True", "true"] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold3()
    end = time.time()
    print(f"Results part {case}: {results}")
    print(f"Runtime: {end - start}")
