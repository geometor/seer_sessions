"""
Extracts a 4x4 subgrid from the input grid if the input is 4x4 or larger.
Otherwise, copies the input grid to the output. The subgrid's upper-left corner
is determined by the left-most, top-most non-zero cell in the input grid.
"""

import numpy as np

def find_upper_left_corner(grid):
    """
    Finds the top-left corner of the smallest rectangle containing all non-zero cells.
    """
    grid = np.array(grid)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r, c)
    return (0, 0) # return (0,0) if we find nothing, as we will copy the input if a 4x4 cannot be extracted.

def transform(input_grid):
    """
    Extracts a 4x4 subgrid or copies the input grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Determine Output Size and Extract or Copy
    if rows >= 4 and cols >= 4:
        # Find the upper-left corner of the subgrid
        corner = find_upper_left_corner(input_grid)
        r_start, c_start = corner

        # Calculate subgrid boundaries.
        r_end = r_start + 4
        c_end = c_start + 4

        # Extract Subgrid
        if r_end <= rows and c_end <= cols:
            output_grid = input_grid[r_start:r_end, c_start:c_end]
        else:
             output_grid = input_grid.copy()

    else:
        # Copy Input
        output_grid = input_grid.copy()

    return output_grid.tolist()