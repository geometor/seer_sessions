"""
Finds a horizontal segment of at least four contiguous blue (1) pixels present in both the second and third rows of the input grid. 
Replaces the segment on rows two and three with a magenta (6) line up to a white (0) pixel or end of row.
"""

import numpy as np

def find_start_column(input_grid):
    """Finds the starting column index of the horizontal segment."""
    rows, cols = input_grid.shape
    for j in range(cols - 3):  # Iterate up to the fourth-to-last column
        # Check for four contiguous blue pixels in both row 1 and row 2
        if (input_grid[1, j:j+4] == 1).all() and (input_grid[2, j:j+4] == 1).all():
            return j
    return -1  # Return -1 if no such segment is found

def find_end_column(input_grid, start_col):
    """finds the column index where we should stop replacing"""
    rows, cols = input_grid.shape
    for j in range(start_col, cols):
        if input_grid[1,j] == 0:
            return j
    return cols


def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the starting column of the horizontal segment
    start_col = find_start_column(input_grid)
    if start_col == -1:
       return output_grid

    # find the end_col
    end_col = find_end_column(input_grid, start_col)

    # Replace the segment with magenta (6) in rows 1 and 2
    output_grid[1, start_col:end_col] = 6
    output_grid[2, start_col:end_col] = 6

    return output_grid