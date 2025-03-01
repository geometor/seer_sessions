"""
The transformation rule identifies a single row within the input grid that consists entirely of blue pixels (value 1). If such a row is found, it is moved to the bottom of the grid. The rows that were originally below the all-blue row are shifted upwards to fill the gap created by the movement of the all-blue row. The all-blue row always moves to the bottom, even if other rows below are all the same color. If there is no all-blue row in the input grid, the grid is not modified.
"""

import numpy as np

def find_all_blue_row(grid):
    """Helper function to find the index of the row with all blue pixels."""
    for i, row in enumerate(grid):
        if np.all(row == 1):
            return i
    return -1

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    num_rows = output_grid.shape[0]

    # Find the row with all blue pixels (value 1)
    blue_row_index = find_all_blue_row(input_grid)

    # If a blue row is found, perform the row shift
    if blue_row_index != -1:
        # Store the all blue row
        blue_row = output_grid[blue_row_index]
        
        # Shift rows down from blue_row_index to num_rows-1
        output_grid[blue_row_index:num_rows-1] = output_grid[blue_row_index+1:num_rows]
        
        # Move the blue row to the bottom
        output_grid[num_rows-1] = blue_row

    return output_grid