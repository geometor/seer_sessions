"""
1. Identify Objects: Scan the input grid to find all distinct, contiguous objects. An object is defined as a group of connected pixels of the same color, excluding black (color 0). Connectivity is defined by the 4 cardinal directions (up, down, left, right).

2. Find Top-Left Corner: For each identified object, determine the coordinates of its top-left corner. This is the pixel within the object that has the smallest row and column indices.

3. Sort by Horizontal Position: Sort the identified objects based on the horizontal position (column index) of their top-left corners. Objects with top-left corners further to the left come first.

4. Create Output Grid: Construct a new 1xN grid, where N is the number of distinct objects found.

5. Populate Output: Iterate through the sorted objects. For each object, get the color of its top-left corner pixel. Place this color value into the output grid at the corresponding index (starting from 0).
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def find_top_left_corner(object_coords):
    """
    Finds the top-left corner coordinates of an object.
    Returns a tuple (row, col).
    """
    min_row = min(r for r, _ in object_coords)
    min_col = min(c for _, c in object_coords)
    return (min_row, min_col)


def transform(input_grid):
    # Find distinct objects
    objects = find_objects(input_grid)

    # Find top-left corners for each object
    top_left_corners = [find_top_left_corner(obj) for obj in objects]

    # Create output grid: height 1, width = number of objects
    num_objects = len(objects)
    output_grid = np.zeros((1, num_objects), dtype=int)

    # Sort objects based on the horizontal position of their top-left corners
    sorted_objects = sorted(zip(objects, top_left_corners), key=lambda x: x[1][1])


    # Populate output grid
    for i, (obj, (r, c)) in enumerate(sorted_objects):
        color = input_grid[r, c]
        output_grid[0, i] = color

    return output_grid