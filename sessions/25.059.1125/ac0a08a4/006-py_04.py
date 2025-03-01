"""
Expands each pixel in the input grid into a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each pixel into a 2x2 block.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = 2 * input_height, 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(input_height):
        for j in range(input_width):
            # Expand each pixel to a 2x2 block in the output grid.
            value = input_grid[i, j]
            output_grid[2*i:2*i+2, 2*j:2*j+2] = value

    return output_grid