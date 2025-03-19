"""
1.  **Input:**  A grid of pixels of varying dimensions.
2.  **Output:** A grid of pixels. The output grid height matches the input grid height. The output grid width is 3 times the input grid width.
3.  **Transformation:** For each pixel in the input grid:
    *   Create a 3x3 block of pixels in the output grid.
    *   The color of the 3x3 block is the same as the original pixel's color.
    *  The top-left corner of the 3 x 3 block will start in the output grid at the same y index as the input pixel, the x index will be the original x index multiplied by 3.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid.  Height is same as input, width is 3x input.
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]
    output_grid = np.zeros((input_height, input_width * 3), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(input_height):
        for j in range(input_width):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Create the 3x3 block. The top-left corner's position is crucial.
            for x in range(3):
                output_grid[i, j*3 + x] = color  # Only need to set one row

    return output_grid