"""
Extracts a 4x4 subgrid from the input grid. The subgrid's upper-right corner
is determined by the right-most, top-most non-zero cell in the input grid.
"""

import numpy as np

def find_upper_right_corner(grid):
    # Iterate through rows from top to bottom
    for r_idx, row in enumerate(grid):
        # Iterate through columns from right to left
        for c_idx in range(len(row) - 1, -1, -1):
            if row[c_idx] != 0:
                return (r_idx, c_idx)
    return None  # Should not happen in valid cases, but handle for safety

def transform(input_grid):
    """
    Extracts a 4x4 subgrid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the upper-right corner of the subgrid
    corner = find_upper_right_corner(input_grid)

    if corner is None:
        return [[]] # Return Empty grid.

    r_start, c_start = corner
    
    # Calculate subgrid boundaries.
    r_end = r_start + 4
    c_end = c_start + 1 # we identified this is incorrect

    # Ensure we don't exceed the original grid boundaries.
    if r_end > rows or c_end > cols:
          return [[]]

    # Extract Subgrid
    # offset the columns by 3 - making subgrid size 4x4
    output_grid = input_grid[r_start:r_end, c_start - 3:c_end]
    
    return output_grid.tolist()