"""
The transformation takes each pixel in the input and expands it into a 2x2 square of the same color in the output. The output is then the expanded result, but inset one pixel from all edges, forming a 0-value border.
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

    # Iterate through input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the pixel value from input
            pixel_value = input_grid[i][j]

            # Duplicate the pixel to form a 2x2 block in the output grid, offset by 1
            output_grid[i+1][j+1] = pixel_value
            output_grid[i+1][j+2] = pixel_value
            output_grid[i+2][j+1] = pixel_value
            output_grid[i+2][j+2] = pixel_value

    return output_grid