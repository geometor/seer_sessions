"""
The input grid is divided into non-overlapping 2x2 blocks. For each block, the pixel values are inspected. IF the block contains a pixel of a pre-determined color, a pixel of that color is output. OTHERWISE, a pixel of a different pre-determined color is output. A new grid is constructed from these selected pixels, with dimensions half that of the input grid.

Previous Rule: If the block contains a green (3) pixel, the output pixel is green (3). Otherwise, the output pixel is blue (1).

This rule is likely incorrect and needs to be refined based on all examples.
"""

import numpy as np

def get_pixel_value(block, value):
    """
    Helper function to return the first index i, j of a value, or -1,-1 if not
    present.
    """
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i,j] == value:
                return i, j
    return -1,-1

def transform(input_grid):
    # convert input to numpy array
    input_grid = np.array(input_grid)
    # get dimensions of input grid
    input_height, input_width = input_grid.shape
    # initialize output grid based on the size of input_grid, divide by 2
    output_height = input_height // 2
    output_width = input_width // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # iterate through 2x2 blocks of the input
    for i in range(output_height):
        for j in range(output_width):
            # Define the 2x2 block in the input grid
            block = input_grid[i*2:(i+1)*2, j*2:(j+1)*2]

            # Check for green (3) in the block - this needs to become general from yaml
            green_row, green_col = get_pixel_value(block, 3)
            if green_row != -1:
                output_grid[i,j] = 3 # Output green
            else:
                output_grid[i,j] = 1   #else output blue

    return output_grid.tolist()