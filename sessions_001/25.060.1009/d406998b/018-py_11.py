"""
Replace gray pixels (value 5) with green pixels (value 3) if the gray pixel is part of a contiguous region of gray pixels that forms a rectangle.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous regions of the same color as objects.
    Returns a list of objects, where each object is a set of (row, col) tuples.
    """
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(row + dr, col + dc, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = set()
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def is_rectangle(object_pixels):
    """
    Checks if a set of pixels forms a rectangle.
    """
    if not object_pixels:
        return False
    rows = [r for r, _ in object_pixels]
    cols = [c for _, c in object_pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check if the number of pixels matches the area of the rectangle
    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
    if len(object_pixels) != expected_size:
        return False

    # Check if all pixels within the bounding box are present
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r, c) not in object_pixels:
                return False
    return True

def transform(input_grid):
    """
    Transforms the input grid by replacing gray pixels (5) with green pixels (3)
    if the gray pixel is part of a contiguous region of gray pixels that forms a rectangle.
    """
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    for obj in objects:
        # Check if the object is gray and a rectangle
        if all(input_grid[r, c] == 5 for r, c in obj) and is_rectangle(obj):
            for r, c in obj:
                output_grid[r, c] = 3  # Replace with green

    return output_grid