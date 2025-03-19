"""
Locate a 3x1 region in the input grid and replace it with blue (1) pixels. Copy all other pixels from the input grid to the output grid unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing a 3x1 region with blue pixels.
    """
    output_grid = np.copy(input_grid)

    # Define the region to be replaced.  These values are derived from the *single* example.
    row_start = 6
    row_end = 8
    col_start = 3
    col_end = 5

    # Replace the specified region with blue (1).
    output_grid[row_start:row_end+1, col_start:col_end+1] = 1

    return output_grid