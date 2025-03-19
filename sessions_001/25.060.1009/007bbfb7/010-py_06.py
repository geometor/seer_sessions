"""
Expands each input pixel into a 3x3 block of the same color.
If the input pixel is orange (7), the 3x3 block is filled with orange,
and the top-left pixel of the block is set to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 3, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Calculate the top-left corner of the corresponding 3x3 block
            # in the output grid
            output_i = i * 3
            output_j = j * 3

            # Fill the 3x3 block with the same color as the input pixel
            output_grid[output_i:output_i+3, output_j:output_j+3] = input_grid[i, j]

            # If the input pixel is orange (7)
            if input_grid[i, j] == 7:
                # Set the top-left pixel to white (0)
                output_grid[output_i, output_j] = 0

    return output_grid