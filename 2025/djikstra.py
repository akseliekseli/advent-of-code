import numpy as np
import heapq
from collections import defaultdict, deque

WALL_NUM = 100000


class Djikstra:
    def __init__(self, file, wall_char="#"):
        self.file = file
        self.wall_char = wall_char
        self.lines = self.file.splitlines()
        self.grid = []
        for ii, line in enumerate(self.lines):
            self.grid.append([])
            for jj, char in enumerate(line):
                if char == self.wall_char:
                    self.grid[ii].append(WALL_NUM)
                else:
                    if char == "S":
                        self.start = (ii, jj)
                    elif char == "E":
                        self.end = (ii, jj)
                    self.grid[ii].append(1)
        self.grid = np.array(self.grid, dtype=float)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def dijkstra(self):
        distances = np.full((self.rows, self.cols), np.inf)
        distances[self.start] = 0
        parents = {self.start: None}
        visited = defaultdict()
        # Priority queue for (distance, (row, col), prev_dir)
        queue = [(0, self.start, None)]
        seats = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            current_distance, (current_row, current_col), prev_dir = heapq.heappop(
                queue
            )
            if (current_row, current_col) == self.end:
                break
            if current_distance > distances[current_row, current_col]:
                continue
            for dir in directions:
                neighbor_row, neighbor_col = current_row + dir[0], current_col + dir[1]
                if self.check_bounds((neighbor_row, neighbor_col)):
                    distance = current_distance + self.grid[neighbor_row, neighbor_col]
                    if prev_dir is not None and dir != prev_dir:
                        distance += 1000
                    if distance < distances[neighbor_row, neighbor_col]:
                        distances[neighbor_row, neighbor_col] = distance
                        parents[(neighbor_row, neighbor_col)] = (
                            current_row,
                            current_col,
                        )
                        heapq.heappush(
                            queue, (distance, (neighbor_row, neighbor_col), dir)
                        )
        path = []
        current = self.end
        while current is not None:
            path.append(current)
            current = parents.get(current)
        path.reverse()
        return path, int(distances[self.end]), distances

    def get_neighbors(self, x, y):
        """
        Get all valid neighbors for a cell in the grid.

        :param x: Row index of the current cell
        :param y: Column index of the current cell
        :return: List of valid neighbor cells (x, y)
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 1:
                neighbors.append(((nx, ny), (dx, dy)))
        return neighbors

    def dijkstra_gold(self):
        distances = np.full((self.rows, self.cols), np.inf)
        distances[self.start] = 0
        parents = {self.start: None}
        seats = {self.start}
        visited = set()
        best_score = np.inf
        # Priority queue for (distance, (row, col), prev_dir)
        queue = [(0, self.start, None, [self.start])]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            current_distance, (current_row, current_col), prev_dir, path = (
                heapq.heappop(queue)
            )
            if current_distance > best_score:
                return seats
            visited.add(((current_row, current_col), prev_dir))
            for dir in directions:
                neighbor_row, neighbor_col = current_row + dir[0], current_col + dir[1]
                distance = current_distance + self.grid[neighbor_row, neighbor_col]
                if self.check_bounds((neighbor_row, neighbor_col)):
                    if prev_dir is not None and dir != prev_dir:
                        distance += 1000
                    if ((neighbor_row, neighbor_col), dir) in visited:
                        continue
                    if (current_row, current_col) == self.end:
                        best_score = current_distance
                        seats.update(path + [(current_row, current_col)])
                    elif distance < distances[(neighbor_row, neighbor_col)]:
                        path_new = path + [(neighbor_row, neighbor_col)]
                        heapq.heappush(
                            queue,
                            (distance, (neighbor_row, neighbor_col), dir, path_new),
                        )

    def compute_path(self, parents):
        path = []
        current = self.end
        while current is not None:
            path.append(current)
            current = parents.get(current)
        path.reverse()
        return path

    def check_bounds(self, point):
        (x, y) = point
        if self.grid[x][y] == WALL_NUM:
            return False
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return True
        else:
            return False
