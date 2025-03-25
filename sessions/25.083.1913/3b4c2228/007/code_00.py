"""
Transforms an input grid into a 3x3 output grid based on the number of unique
colors present in the input grid's objects. The output grid contains 1s at
specific positions determined solely by the unique color count, and 0s
elsewhere.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects (contiguous regions of the same non-zero color) in a grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, color, current_object):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                current_object = []
                dfs(r, c, grid[r][c], current_object)
                objects.append(current_object)
    return objects

def get_object_colors(grid, objects):
    """
    Returns a list of the color of each object.
    """
    colors = []
    for obj in objects:
        color = grid[obj[0][0]][obj[0][1]]
        colors.append(color)

    return colors

def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid based on the number of unique colors.
    """
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find distinct objects
    objects = find_objects(input_grid)

    # Get colors of objects
    object_colors = get_object_colors(input_grid, objects)

    # Determine unique object color count
    unique_color_count = len(set(object_colors))

    # change output pixels based on the number of distinct object colors
    if unique_color_count >= 1:
        output_grid[0, 0] = 1
    if unique_color_count == 2:
        output_grid[1, 1] = 1
    if unique_color_count == 3:
        output_grid[1, 1] = 1
        output_grid[2, 2] = 1

    return output_grid