"""
1. For a 3x3 input grid:
2. Set all pixels in the first column (column 0) to white (0).
3. Set all pixels in the last column (column 2) to white (0).
4. All other pixels should retain their original color and position.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = input_grid.copy()
    
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape
    
    # Apply rules only if the grid is 3x3
    if rows == 3 and cols == 3:
        # Set all pixels in the first column (column 0) to white (0).
        output_grid[:, 0] = 0
        # Set all pixels in the last column (column 2) to white (0).
        output_grid[:, 2] = 0

    # Return the modified grid
    return output_grid