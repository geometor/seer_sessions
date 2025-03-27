"""
Expands the input grid to double its dimensions and replaces each gray pixel (5) with a 2x2 checkerboard pattern of blue (1) and red (2) pixels. White pixels (0) are expanded to 2x2 white blocks.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with doubled dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid
    for i in range(input_height):
        for j in range(input_width):
            # Preserve Whites (0 -> 0) in a 2x2 block
            if input_grid[i, j] == 0:
                output_grid[2*i:2*i+2, 2*j:2*j+2] = 0
            # Map Gray (5) to a 2x2 checkerboard of Blue (1) and Red (2)
            elif input_grid[i, j] == 5:
                output_grid[2*i, 2*j] = 1
                output_grid[2*i, 2*j+1] = 2
                output_grid[2*i+1, 2*j] = 2
                output_grid[2*i+1, 2*j+1] = 1

    return output_grid