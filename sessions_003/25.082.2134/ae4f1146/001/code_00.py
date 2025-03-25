"""
The rule extracts a 3x3 subgrid within the 9x9 input grid, where it contains all the non-white color pixels.
"""

import numpy as np

def find_subgrid(input_grid):
    # Iterate through all possible 3x3 subgrids
    for row_start in range(input_grid.shape[0] - 2):
        for col_start in range(input_grid.shape[1] - 2):
            subgrid = input_grid[row_start:row_start+3, col_start:col_start+3]
            # Check if the subgrid contains only non-zero (non-white) pixels
            if np.all(subgrid != 0):
                return subgrid
    return None  # Return None if no such subgrid is found


def transform(input_grid):
    """
    Transforms a 9x9 input grid into a 3x3 output grid by extracting a 3x3 subgrid.
    The chosen subgrid is the one that contains no white(0) pixels.
    """
    # Find the 3x3 subgrid
    output_grid = find_subgrid(np.array(input_grid))
    
    if output_grid is None:
        # handle edge case, return a grid with 0's
        output_grid = np.zeros((3,3),dtype=int)

    return output_grid.tolist()