"""
The transformation rule is: Divide the input grid into non-overlapping 3x3 blocks. For each 3x3 block, select the color value of the center pixel. Construct the output grid by placing the selected center pixel values in a corresponding grid, maintaining their relative positions. Ignore background color of 'white'(0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.  Since input is 9x9 and we are reducing 3x3 blocks to single pixels, the output will be 3x3.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the input grid in 3x3 steps, effectively dividing it into 3x3 blocks.
    for i in range(0, input_grid.shape[0], 3):
        for j in range(0, input_grid.shape[1], 3):
            # Extract the center pixel value of the current 3x3 block.
            center_pixel = input_grid[i+1, j+1]
           
            # Place the center pixel value into the corresponding position in the output grid.
            output_grid[i//3, j//3] = center_pixel

    return output_grid