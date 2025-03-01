"""
Transforms an input grid into a larger output grid by expanding each non-zero pixel into a 4x4 block.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Grid Size
    input_height, input_width = input_grid.shape
    output_height = input_height * 4
    output_width = input_width * 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Pixel Expansion
    for y in range(input_height):
        for x in range(input_width):
            pixel_value = input_grid[y, x]
            if pixel_value != 0:
                # Calculate output coordinates
                out_x = x * 4
                out_y = y * 4

                # Create 4x4 block
                output_grid[out_y:out_y+4, out_x:out_x+4] = pixel_value

    return output_grid