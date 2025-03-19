"""
The transformation extracts a 2x2 subgrid from the input grid. This subgrid appears
to be selected based on the position of the non-azure (non-8) pixels. The subgrid is
chosen such that it starts from the bottom-most and left-most non-8 pixel, going one
row up, and extending one column to the right.
"""

import numpy as np

def find_bottom_left_non_8(grid):
    """Finds the row and column index of the bottom-most, left-most non-8 pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            if grid[r, c] != 8:
                return r, c
    return None  # Should not happen in these tasks, as there's always a non-8 pixel

def transform(input_grid):
    """Extracts a 2x2 subgrid based on bottom-left non-8 pixel."""
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bottom-left non-8 pixel
    start_row, start_col = find_bottom_left_non_8(input_grid)

    # Extract the 2x2 subgrid
    output_grid = input_grid[start_row-1:start_row+1, start_col:start_col+2]
    
    return output_grid.tolist()