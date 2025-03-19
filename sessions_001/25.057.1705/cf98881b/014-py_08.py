"""
The transformation extracts the first column of the input grid. Then constructs the output grid by
creating L shape of yellow(4), with a maroon (9) in between the arms of the L.
The non yellow pixels from the first column of the input grid, are placed at top of first column, with
the second pixel below. The rest is filled with maroon.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as all maroon (9)
    output_grid = np.full((4, 4), 9, dtype=int)

    # Create the L shape of yellow (4)
    for i in range(4):
        output_grid[i, 0] = 4  # Vertical part of L
        output_grid[3, i] = 4  # Horizontal part of L
        
    # Extract the first column of the input grid
    first_column = input_grid[:, 0]

    # Find pixels in the first column that are not yellow (4)
    special_pixels = []
    for pixel in first_column:
        if pixel != 4:
            special_pixels.append(pixel)

    # Place special pixels in the output grid's first column
    row_index = 0
    for pixel in special_pixels:
        if row_index < 4:
            output_grid[row_index, 0] = pixel
            row_index += 1
        else:
            break #stop if there's more pixels than we can place

    return output_grid