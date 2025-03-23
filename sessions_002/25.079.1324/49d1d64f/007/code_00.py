"""
The transformation copies the input grid into the output grid, offsetting it by one row and one column to create a border of 0s around the copied input.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of input grid
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Initialize output_grid with zeros, 2 rows and 2 columns larger than input
    output_rows = input_rows + 2
    output_cols = input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input grid and copy each pixel to output, offset by 1
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the pixel value from the input
            pixel_value = input_grid[i][j]

            # Copy the pixel to output grid with an offset of (1,1)
            output_grid[i+1][j+1] = pixel_value

    return output_grid