def get_neighbors(point, rows, cols):
    # Use a kernel to calculate next points and check if they are inbounds
    x, y = point
    kernel = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = [(x + dx, y + dy) for dx, dy in kernel]
    neighbors = [(x, y) for x, y in neighbors if check_bounds((x, y), rows, cols)]
    return neighbors


def get_next_num():
    for ii in range(1, 10):
        yield ii


def check_bounds(point, rows, cols):
    (x, y) = point
    if 0 <= x < rows and 0 <= y < cols:
        return True


def get_diag_neighbors(point):
    kernel_diag = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
    x, y = point
    return [(x + dx, y + dy) for dx, dy in kernel_diag]


def check_quadrant(point, rows, cols):
    (x, y) = point
    if x == cols // 2 or y == rows // 2:
        pass
    elif x < cols // 2 and y < rows // 2:
        quadrand_sums[0] += 1
    elif x < cols // 2 and y > rows // 2:
        quadrand_sums[1] += 1
    elif x > cols // 2 and y < rows // 2:
        quadrand_sums[2] += 1
    elif x > cols // 2 and y > rows // 2:
        quadrand_sums[3] += 1
