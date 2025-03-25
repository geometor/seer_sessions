"""
The transformation rule expands a 3x3 input grid into a 9x9 output grid. Each pixel in the input
grid creates a 3x3 block of the same color in the output grid, with the top-left corner of the block
positioned at 3 times the row and column index of the input pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 9x9 filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through the 3x3 input grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Get the color of the current pixel
            pixel_color = input_grid[r, c]

            # Calculate offset for the 3x3 block
            offset_r = r * 3
            offset_c = c * 3

            # Fill the 3x3 block in the output grid with the same color
            output_grid[offset_r:offset_r + 3, offset_c:offset_c + 3] = pixel_color

    return output_grid