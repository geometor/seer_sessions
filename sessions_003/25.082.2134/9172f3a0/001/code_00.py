"""
The transformation rule is to expand each pixel of the input grid into a 3x3 block of the same color in the output grid, effectively creating a scaled-up version of the input.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Initialize output grid with dimensions 3 times the input
    output_rows = input_rows * 3
    output_cols = input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each cell in the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the color of the current input cell
            color = input_grid[i][j]

            # Fill the corresponding 3x3 block in the output grid
            for row_offset in range(3):
                for col_offset in range(3):
                    output_grid[i * 3 + row_offset][j * 3 + col_offset] = color

    return output_grid