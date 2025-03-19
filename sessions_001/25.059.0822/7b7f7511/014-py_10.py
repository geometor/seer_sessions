"""
The transformation rule halves the width of the input grid. For each row, and each pair of adjacent columns (2*j and 2*j+1) in the input grid, the corresponding element in output at j is the *maximum* of input element values at column 2*j and 2*j+1 of that row. The output grid's height remains the same as the input grid's.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    new_cols = cols // 2
    output_grid = np.zeros((rows, new_cols), dtype=int)

    # Change output pixels 
    for i in range(rows):
        for j in range(new_cols):
            # Calculate the maximum of the two corresponding input pixels
            output_grid[i][j] = max(input_grid[i][2*j], input_grid[i][2*j + 1])

    return output_grid