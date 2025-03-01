"""
The transformation extracts and rearranges gray (5) shapes from the input grid to create a condensed 9x9 representation in the output grid, preserving some spatial relationships and relative positions.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def transform(input_grid):
    """
    Transforms input_grid to condensed 9x9 output_grid.
    Extract gray objects and redraw.
    """
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Find gray objects
    gray_objects = find_objects(input_grid, 5)
    
    # Extract and project pattern into smaller grid
    # simple version - just project pixels by scaling x and y
    for obj in gray_objects:
       for r,c in obj:
          out_r = int(r * 9 / input_grid.shape[0])
          out_c = int(c * 9 / input_grid.shape[1])
          output_grid[out_r,out_c] = 5

    return output_grid