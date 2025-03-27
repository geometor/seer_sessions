"""
Counts the number of occurrences of a 3x3 "X" pattern within a given input grid.
An "X" pattern is defined as a 3x3 grid where:
- The four corner cells (diagonals) have the same non-zero color.
- The center cell has a different color than the diagonal cells or is zero.
- The edge cells adjacent to the center are a different color or zero.
"""

import numpy as np

def is_x(grid):
    """Checks if a 3x3 grid is an 'X'."""
    if grid.shape != (3, 3):
        return False

    center = grid[1, 1]
    diag_val = grid[0, 0]

    if center == diag_val or diag_val == 0:
        return False  # Center and diagonals cannot be same or zero.

    if grid[0,2] != diag_val or grid[2,0] != diag_val or grid[2,2] != diag_val:
        return False

    if grid[0,1] == diag_val or grid[1,0] == diag_val or grid[1,2]==diag_val or grid[2,1] == diag_val:
        return False

    return True

def transform(input_grid):
    """
    Counts the occurrences of the "X" pattern in the input grid.
    """
    grid = np.array(input_grid)
    count = 0
    rows, cols = grid.shape
    # Iterate through all possible 3x3 subgrids
    for i in range(rows - 2):
        for j in range(cols - 2):
            subgrid = grid[i:i+3, j:j+3]
            # Check if the subgrid is an "X"
            if is_x(subgrid):
                count += 1
    return count