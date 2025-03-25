"""
Copies the input grid to the output, and adds a yellow pixel at the bottom of each
column if there is a vertical line of at least two contiguous pixels with
the same non-zero color above it.
"""

import numpy as np

def get_vertical_lines(grid):
    """
    Checks each column for vertical lines of same, non-zero color.
    Returns a list of column indices where such lines exist.
    """
    rows, cols = grid.shape
    valid_columns = []
    for c in range(cols):
        for r in range(rows - 1):  # Check for lines of at least length 2
            if grid[r,c] != 0 and grid[r, c] == grid[r + 1, c]:
                valid_columns.append(c)
                break # move onto the next column once line detected
    return valid_columns

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find columns that have qualifying vertical lines
    valid_columns = get_vertical_lines(input_grid)

    # Add yellow pixel to the bottom of valid columns
    for col in valid_columns:
        output_grid[rows - 1, col] = 4

    return output_grid