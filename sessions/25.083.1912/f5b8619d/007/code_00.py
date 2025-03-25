"""
The transformation rule doubles the dimensions of the input grid. Each pixel in the input grid is transformed into a 2x2 block in the output grid based on these rules:
1.  If the input pixel is 0, the 2x2 block is:
    8 I
    8 8
    where 'I' is the value of the pixel immediately to the right in the input grid. If there is no pixel to the right, I = 8.
2.  If the input pixel is non-zero (N), the 2x2 block is:
    N 8
    8 N
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with dimensions (input_height * 2, input_width * 2)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height * 2, input_width * 2), dtype=int)

    # Iterate through the input grid and expand each pixel
    for row in range(input_height):
        for col in range(input_width):
            # Get the current pixel value
            current_pixel = input_grid[row, col]

            # Determine the 2x2 block based on the current pixel
            if current_pixel == 0:
                # Find 'I' (pixel to the right, or 8 if it doesn't exist)
                i_value = input_grid[row, col + 1] if col + 1 < input_width else 8
                output_grid[row*2, col*2] = 8
                output_grid[row*2, col*2 + 1] = i_value
                output_grid[row*2 + 1, col*2] = 8
                output_grid[row*2 + 1, col*2 + 1] = 8
            else:
                output_grid[row*2, col*2] = current_pixel
                output_grid[row*2, col*2 + 1] = 8
                output_grid[row*2 + 1, col*2] = 8
                output_grid[row*2 + 1, col*2 + 1] = current_pixel

    return output_grid