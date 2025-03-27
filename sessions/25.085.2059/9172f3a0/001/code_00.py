"""
Scales the input grid by a factor of 3 in both height and width.
Each pixel in the input grid is expanded into a 3x3 block of the same color
in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling each pixel into a 3x3 block.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape

    # Calculate the dimensions of the output grid (3 times larger)
    output_H = 3 * H
    output_W = 3 * W

    # Initialize the output grid with zeros (or any default value)
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Iterate through each pixel (r, c) in the input grid
    for r in range(H):
        for c in range(W):
            # Get the color C of the pixel at input_grid[r][c]
            color = input_np[r, c]

            # Calculate the starting row and column for the 3x3 block in the output grid
            output_r_start = 3 * r
            output_c_start = 3 * c

            # Fill the 3x3 block in the output grid with the color C
            # The block spans rows from output_r_start to output_r_start + 2
            # and columns from output_c_start to output_c_start + 2
            output_grid[output_r_start:output_r_start + 3, output_c_start:output_c_start + 3] = color

    # Return the resulting output grid
    return output_grid
