"""
Finds the smallest repeating rectangular sub-grid that, when tiled, reconstructs the input grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by finding the smallest repeating sub-grid."""
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Iterate through all possible sub-grid sizes.
    for sub_rows in range(1, rows + 1):
        for sub_cols in range(1, cols + 1):
            # Check if sub-grid dimensions are valid divisors of the input grid dimensions.
            if rows % sub_rows == 0 and cols % sub_cols == 0:
                sub_grid = grid[:sub_rows, :sub_cols]
                
                # Reconstruct the grid using the current sub_grid.
                reconstructed_grid = np.tile(sub_grid, (rows // sub_rows, cols // sub_cols))
                
                # Check for match.
                if np.array_equal(grid, reconstructed_grid):
                    return sub_grid
    
    # Default: Should not happen if the logic is correct but keep the return
    # for cases there's no repeating pattern, return the 1,1
    return grid[0,0].reshape(1,1)