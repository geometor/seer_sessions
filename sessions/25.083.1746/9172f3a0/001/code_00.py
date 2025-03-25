"""
The transformation rule is to scale up the input grid by a factor of 3. Each pixel in the input grid is replicated to create a 3x3 block in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Calculate output dimensions
    output_rows = input_rows * 3
    output_cols = input_cols * 3

    # Initialize output grid with zeros
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input pixels and replicate
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the color of the current input pixel
            color = input_grid[i][j]
            # Replicate the pixel to a 3x3 block in the output grid
            for row_offset in range(3):
                for col_offset in range(3):
                    output_grid[i*3 + row_offset][j*3 + col_offset] = color

    return output_grid