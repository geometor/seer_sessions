"""
The transformation rule is to double the size of the grid and expand each original pixel into a 2x2 square of the same color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for row in range(input_height):
        for col in range(input_width):
            # Replicate the pixel's color to form a 2x2 block
            output_grid[row*2:row*2+2, col*2:col*2+2] = input_grid[row, col]

    return output_grid