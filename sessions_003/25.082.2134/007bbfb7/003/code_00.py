"""
Expand a 3x3 input grid to a 9x9 output grid by creating a mask and tiling.
The mask is created by finding the intersection of rows and columns with any non-zero values.
The intersection is implemented using an outer product of boolean row and col vectors.
The original grid is then modified by setting elements to 0 if the corresponding mask cell is False.
The output is formed by tiling the modified grid in a 3x3 pattern.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Identify non-zero rows and columns
    non_zero_rows = np.any(input_grid != 0, axis=1)
    non_zero_cols = np.any(input_grid != 0, axis=0)
    
    # Create the intersection mask using outer product
    intersection_mask = np.outer(non_zero_rows, non_zero_cols)
    
    # Apply the mask to modify the grid
    modified_grid = input_grid * intersection_mask

    # Tile the modified grid 3x3
    output_grid = np.tile(modified_grid, (3, 3))

    return output_grid.tolist()