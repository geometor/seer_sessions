"""
Classifies the input grid based on the arrangement of red (2) pixels and returns a corresponding integer.

1.  Examine the input grid.
2.  Classify the input based on the following:
    a. If the red (2) pixels are present in the corners, the value is 1.
    b. If the red (2) pixels are side by side as pairs, the value is 7.
"""

import numpy as np

def check_corners(grid):
    """Checks if the corners of the grid have red pixels."""
    rows, cols = grid.shape
    if (grid[0, 0] == 2 or grid[0, cols - 1] == 2 or
        grid[rows - 1, 0] == 2 or grid[rows - 1, cols - 1] == 2):

        # check that there are not pairs
        has_pair = False
        for i in range(rows):
            for j in range(cols - 1):
                if grid[i,j] == 2 and grid[i, j+1] == 2:
                    has_pair = True
        for i in range(rows - 1):
            for j in range(cols):
                if grid[i,j] == 2 and grid[i+1, j] == 2:
                    has_pair = True
        if not has_pair:
            return True
    return False

def check_pairs(grid):
    """Checks if red pixels are side by side in pairs (horizontally or vertically)."""
    rows, cols = grid.shape
    # Check horizontal pairs
    for i in range(rows):
        for j in range(cols - 1):
            if grid[i, j] == 2 and grid[i, j + 1] == 2:
                return True
    # Check vertical pairs
    for i in range(rows - 1):
        for j in range(cols):
            if grid[i, j] == 2 and grid[i + 1, j] == 2:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid based on red pixel arrangement."""
    grid = np.array(input_grid)

    # Check for corner arrangement
    if check_corners(grid):
        return 1
    # Check for pairs arrangement
    elif check_pairs(grid):
        return 7
    # Default case (should not normally happen based on given train examples).
    else:
      return 0