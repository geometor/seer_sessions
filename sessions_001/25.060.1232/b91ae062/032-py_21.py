"""
Expands each pixel in the input grid into a 4x4 block of the same color in the output grid, maintaining relative positioning.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each pixel into a 4x4 block.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 4, input_width * 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for row in range(input_height):
        for col in range(input_width):
            color = input_grid[row, col]
            # Calculate the top-left corner of the corresponding 4x4 block in the output grid
            output_row_start = row * 4
            output_col_start = col * 4
            # Fill the 4x4 block with the pixel's color
            output_grid[output_row_start:output_row_start + 4, output_col_start:output_col_start + 4] = color

    return output_grid