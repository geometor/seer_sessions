"""
The transformation rule is to double the size of the input grid, replicate each non-zero pixel in the input grid as a 2x2 block of the same color in the output grid, and draw a blue (1) cross centered in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with doubled dimensions and filled with zeros.
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate non-zero pixels as 2x2 blocks.
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] != 0:
                color = input_grid[r, c]
                output_grid[2*r:2*r+2, 2*c:2*c+2] = color

    # Draw a blue (1) cross spanning the entire output grid.
    center_row = output_height // 2
    center_col = output_width // 2

    for i in range(output_height):
        output_grid[i, center_col] = 1
    for i in range(output_width):
        output_grid[center_row,i]=1


    return output_grid