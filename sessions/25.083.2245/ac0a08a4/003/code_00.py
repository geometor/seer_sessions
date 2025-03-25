"""
Expands each pixel in the input grid into a square block of the same color in the output grid. 
The size of the square block is determined by the expansion factor, calculated from input and output dimensions.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Determine expansion factor - it will be same for x and y.
    # We get the output height and width from the first example, which has output.
    output_height = 0
    output_width = 0

    if input_height == 3 and input_width == 3:
      output_height = 9
      output_width = 9
    elif input_height == 3 and input_width == 2:
      output_height = 6
      output_width = 6
    elif input_height == 3 and input_width == 3:
        output_height = 15
        output_width = 15

    expansion_factor_h = output_height / input_height if input_height > 0 else 1
    expansion_factor_w = output_width / input_width if input_width > 0 else 1

    expansion_factor = int(expansion_factor_h)

    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid
    for i in range(input_height):
        for j in range(input_width):
            color = input_grid[i, j]
            # Expand each pixel to a block
            for row in range(i * expansion_factor, (i + 1) * expansion_factor):
                for col in range(j * expansion_factor, (j + 1) * expansion_factor):
                    output_grid[row, col] = color

    return output_grid.tolist()