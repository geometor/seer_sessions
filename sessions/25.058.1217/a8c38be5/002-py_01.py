"""
Transforms an input grid by extracting all contiguous non-zero objects, and
constructing a new grid that contains only these objects, preserving their
relative spatial relationships, but removing all background (zero-valued) pixels.
The output grid's size is determined by the bounding box that encompasses all
extracted objects.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies and returns a list of objects in the grid.  Each object
    is represented as a dictionary containing the coordinates and color
    of its constituent pixels.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c, grid[r][c]))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def bounding_box(objects):
    """
    Calculates the bounding box that encompasses all objects.
    Returns (min_row, max_row, min_col, max_col).
    """
    if not objects:
        return 0, -1, 0, -1  # Empty grid case

    min_row = float('inf')
    max_row = float('-inf')
    min_col = float('inf')
    max_col = float('-inf')

    for obj in objects:
        for r, c, _ in obj:
            min_row = min(min_row, r)
            max_row = max(max_row, r)
            min_col = min(min_col, c)
            max_col = max(max_col, c)

    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    grid = np.array(input_grid)
    objects = find_objects(grid)
    min_row, max_row, min_col, max_col = bounding_box(objects)

    # Calculate output grid dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize the output grid with zeros (background)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place objects in the output grid.
    for obj in objects:
        for r, c, color in obj:
            # Calculate the new position relative to the bounding box
            new_r = r - min_row
            new_c = c - min_col
            output_grid[new_r, new_c] = color

    return output_grid.tolist()