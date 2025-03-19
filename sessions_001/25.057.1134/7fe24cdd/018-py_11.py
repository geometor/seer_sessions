"""
1.  **Determine Output Size:** Calculate the dimensions of the output grid. The
    output grid's height and width are twice the height and width of the input
    grid, respectively.
2.  **Pixel Replication:** For each pixel in the input grid, replicate its
    value in a 2x2 block in the output grid. The top-left corner of this 2x2
    block corresponds to the position of the input pixel, scaled by a factor of
    2 in both the row and column indices. Specifically, if an input pixel is
    at `input_grid[row, col]`, the corresponding 2x2 block in the output grid
    will have its top-left corner at `output_grid[2*row, 2*col]`.
3.  **Output Grid:** The function outputs a grid which has exactly twice the
    dimensions of the input grid in length and width.
"""

import numpy as np

def transform(input_grid):
    # Determine input grid dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Determine output grid dimensions (twice the input)
    output_height = 2 * input_height
    output_width = 2 * input_width

    # Initialize output_grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid
    for row in range(input_height):
        for col in range(input_width):
            # Copy each pixel value
            pixel_value = input_grid[row, col]

            # Create the 2x2 block
            output_grid[2*row, 2*col] = pixel_value
            output_grid[2*row + 1, 2*col] = pixel_value
            output_grid[2*row, 2*col + 1] = pixel_value
            output_grid[2*row + 1, 2*col + 1] = pixel_value

    return output_grid