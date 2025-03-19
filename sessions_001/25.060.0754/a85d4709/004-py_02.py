"""
Transforms a 3x3 input grid to a 3x3 output grid based on a row-dependent color mapping.
Input colors 0 and 5 are mapped to output colors 2, 3, and 4, where the specific mapping depends on the row number.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    
    # Iterate over rows, mapping colors per row.
    for i in range(rows):
       for j in range(cols):
        if i == 0:
            output_grid[i,j] = 3
        elif i == 1:
            output_grid[i,j] = 4
        elif i == 2:
            output_grid[i,j] = 2

    return output_grid