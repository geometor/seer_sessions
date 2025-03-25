"""
The transformation rule involves identifying non-white objects in the input grid and mirroring them vertically. 
Objects above the center line of the grid are duplicated below the center line, maintaining their relative positions.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-zero pixels as objects.
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
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r, c], current_object))  # Store color and object pixels
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row = rows // 2

    # Find objects
    objects = find_objects(input_grid)

    # Duplicate objects from above center_row to below
    for color, obj_pixels in objects:
        for r, c in obj_pixels:
            if r < center_row:  # if it's above center
                mirror_r = rows - 1 - r  # find bottom of grid
                if output_grid[mirror_r,c] == 0:
                    output_grid[mirror_r, c] = color  # set the color in the mirrored position
            elif r == center_row:
                mirror_r = rows - 1 - r  # find bottom of grid
                if output_grid[mirror_r,c] == 0:
                   output_grid[mirror_r, c] = color  # set the color in the mirrored position

    return output_grid.tolist()