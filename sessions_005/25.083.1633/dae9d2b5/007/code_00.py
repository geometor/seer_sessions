"""
Transforms an input grid by replacing yellow (4) and green (3) pixels with magenta (6),
and then extracting the smallest subgrid containing all non-white pixels.
"""

import numpy as np

def get_bounding_box(grid):
    """
    Finds the bounding box of non-white pixels in a grid.
    Returns (min_row, max_row, min_col, max_col).
    If no non-white pixels are found, returns (rows, cols, -1, -1).
    """
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid according to the rules.
    """
    # Create a copy of the input grid to perform color substitution.
    modified_grid = np.copy(input_grid)

    # Perform color substitution.
    for i in range(modified_grid.shape[0]):
        for j in range(modified_grid.shape[1]):
            if modified_grid[i, j] == 4:  # Yellow
                modified_grid[i, j] = 6  # Magenta
            elif modified_grid[i, j] == 3:  # Green
                modified_grid[i, j] = 6  # Magenta

    # Find the bounding box of non-white pixels.
    min_row, max_row, min_col, max_col = get_bounding_box(modified_grid)

    if min_row > max_row or min_col > max_col:
        return np.zeros((0, 0), dtype=int) # Return empty if not found

    # Extract the subgrid.
    output_grid = modified_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid