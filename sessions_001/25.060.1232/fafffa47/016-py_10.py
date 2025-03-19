"""
The input grid is reduced to half its height while maintaining the same width. Maroon(9) pixels in the top half of the input grid are transformed to red(2) in the output grid in a horizontally mirrored position, while a blue(1) pixel causes transformation to red(2) on the next row down at the same location in the bottom half. White(0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Color Transformation (Top Half)
    for i in range(output_height):
        for j in range(input_width):
            if input_grid[i, j] == 9:
                output_grid[i, input_width - 1 - j] = 2

    # Color Transformation (Bottom Half)
    for i in range(output_height, input_height):
        for j in range(input_width):
          if input_grid[i, j] == 1:
              if i-output_height >=0 and i-output_height < output_height:
                output_grid[i-output_height,j] = 2
                
    # White Retention (Implicit, as we initialize with 0)

    return output_grid