"""
The transformation takes each pixel in the input grid and expands it into a 2x2 square of the same color in the output grid. The output is surrounded by a border of 0-value pixels.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of input grid
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Initialize output_grid with zeros, 1 row and 1 column larger than input * 2
    output_rows = input_rows * 2 + 2
    output_cols = input_cols * 2 + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the pixel value from input
            pixel_value = input_grid[i][j]

            # Map the input pixel to the output, offset by 1 for border, and expand 2x2
            output_grid[i*2+1][j*2+1] = pixel_value
            output_grid[i*2+1][j*2+2] = pixel_value
            output_grid[i*2+2][j*2+1] = pixel_value
            output_grid[i*2+2][j*2+2] = pixel_value

    return output_grid