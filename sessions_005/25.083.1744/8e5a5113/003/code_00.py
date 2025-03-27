"""
The transformation takes the left side of the input grid (everything left of the gray '5' column) and mirrors it onto the right side of the output grid, using the '5' column as the mirroring axis. The columns to the right of the second '5' column remain unchanged.
"""

import numpy as np

def find_mirror_column(grid):
    # Iterate through columns to find the one with all '5's.
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen

def transform(input_grid):
    """
    Transforms the input grid by mirroring the left side to the right side,
    using the column of '5's as the mirror.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    mirror_col = find_mirror_column(input_grid)
    
    if mirror_col == -1:
        return output_grid.tolist() # Return original if no mirror column

    # Iterate through rows
    for i in range(input_grid.shape[0]):
        # Iterate from mirror_col to end of row on the right side
        k = 1
        for j in range(mirror_col + 1, 2*mirror_col+1):
            output_grid[i, j] = input_grid[i, mirror_col - k]
            k += 1

    
    return output_grid.tolist()