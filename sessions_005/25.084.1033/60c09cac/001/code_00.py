"""
Scales the input grid by a factor of 2 in both height and width. 
Each pixel in the input grid is expanded into a 2x2 block of the same color 
in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling it up by a factor of 2.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the scaled output grid.
    """
    # Determine the height (H_in) and width (W_in) of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid: height (H_out) = 2 * H_in, width (W_out) = 2 * W_in.
    output_height = 2 * input_height
    output_width = 2 * input_width

    # Create a new output grid of size H_out x W_out, initialized with 0s (white).
    # Using the same dtype as the input grid is good practice.
    output_grid = np.zeros((output_height, output_width), dtype=input_grid.dtype)

    # Iterate through each pixel located at (row, col) in the input grid.
    for row in range(input_height):
        for col in range(input_width):
            # Identify the color C of the input pixel at (row, col).
            color = input_grid[row, col]

            # Determine the corresponding top-left coordinate (out_row, out_col) in the output grid.
            out_row = 2 * row
            out_col = 2 * col

            # Fill the 2x2 block of pixels in the output grid starting at (out_row, out_col) with the color C.
            output_grid[out_row, out_col] = color         # Top-left
            output_grid[out_row, out_col + 1] = color     # Top-right
            output_grid[out_row + 1, out_col] = color     # Bottom-left
            output_grid[out_row + 1, out_col + 1] = color # Bottom-right

    # Return the fully constructed output grid.
    return output_grid