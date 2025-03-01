"""
The input grid is scanned for the presence of a single non-zero pixel. If a non-zero pixel is found, its value and its row index within the input grid are recorded.  A 3x3 output grid is created and filled with zeros.  If a non-zero pixel was found in the input, the output grid's center column (index 1) is set to the non-zero value at the row corresponding to the input row divided by 3 (integer division).  If no non-zero pixel is found, the output grid remains all zeros.
"""

import numpy as np

def find_nonzero_pixel(grid):
    """Finds the first non-zero pixel in a grid and returns its value and row index."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                return grid[i, j], i
    return 0, -1  # Return 0 and -1 if no non-zero pixel is found

def transform(input_grid):
    # Initialize output_grid as a 3x3 array filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the first non-zero pixel in the input grid.
    value, row_index = find_nonzero_pixel(input_grid)

    # If a non-zero pixel was found, set the corresponding output pixel.
    if value != 0:
        output_row = row_index // 3
        output_grid[output_row, 1] = value

    return output_grid