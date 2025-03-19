"""
Transforms the input grid based on the presence of a 2x2 red square. If the red square is present, the output is identical to the input.
"""

import numpy as np

def find_red_square(grid):
    # Find the top-left corner coordinates of the red square
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r, c+1] == 2 and grid[r+1, c+1] == 2:
                return (r, c)  # Return top-left corner
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Find the red square
    red_square_corner = find_red_square(input_grid)

    # If a red square is present, return the input grid
    if red_square_corner is not None:
        return output_grid

    # If no red square, the output is (currently) undefined, but for these
    # test cases, it is still a copy of input (this will need to change if we had examples that lack a red square)
    
    return output_grid