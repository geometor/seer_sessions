"""
Transforms a 3x3 input grid into a 5x3 output grid based on column-wise rules.
The first element of each input column dictates the values in the corresponding output column,
with specific expansion and zero-filling rules.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a 5x3 array filled with zeros.
    output_grid = np.zeros((5, 3), dtype=int)

    # First Column Transformation
    output_grid[:, 0] = input_grid[0, 0]

    # Second Column Transformation
    output_grid[:3, 1] = input_grid[0, 1]
    output_grid[3:, 1] = 0  # Already 0, but explicit for clarity

    # Third Column Transformation
    output_grid[0, 2] = input_grid[0,2]
    output_grid[1:, 2] = 0  # Already 0 due to initialization, but explicit.
    
    return output_grid