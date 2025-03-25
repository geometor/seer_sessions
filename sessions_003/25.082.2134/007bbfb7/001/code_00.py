"""
The input grid is expanded into a 9x9 output grid. The output grid is created by
tiling a modified version of the input grid. The modification involves setting
certain pixels in the input grid to 0 based on whether their corresponding row
and column contain any non-zero values. Rows and columns that are all zeros
remain all zeros.  Rows and columns that contain any non-zero values are kept, all other rows and cols are zeroed. The modified input grid is then tiled 3x3
times to form the output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    modified_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify non-zero rows and columns
    non_zero_rows = np.any(input_grid != 0, axis=1)
    non_zero_cols = np.any(input_grid != 0, axis=0)
    
    # Create mask
    mask = np.zeros_like(input_grid, dtype=bool)
    for r in range(rows):
        for c in range(cols):
           if non_zero_rows[r] and non_zero_cols[c]:
                mask[r,c] = True

    # Apply the mask
    modified_grid[~mask] = 0

    # Tile the modified grid
    output_grid = np.tile(modified_grid, (3, 3))
    return output_grid.tolist()