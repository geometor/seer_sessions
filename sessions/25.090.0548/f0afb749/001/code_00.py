"""
Transforms an input grid by scaling it by a factor of 2 in both dimensions.
Each pixel in the input grid maps to a 2x2 block in the output grid.
If the input pixel's color is not white (0), the corresponding 2x2 output block is filled entirely with that color.
If the input pixel's color is white (0), the corresponding 2x2 output block is filled with a specific pattern:
- Top-left: blue (1)
- Top-right: white (0)
- Bottom-left: white (0)
- Bottom-right: blue (1)
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Determine the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid, filling with white (0) by default might be useful
    # although every pixel will be overwritten anyway based on the logic.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_grid[r, c]
            
            # Determine the top-left coordinates of the corresponding 2x2 block in the output grid
            out_r = 2 * r
            out_c = 2 * c

            # Apply the transformation rule based on the input pixel color
            if input_color != 0:
                # Non-white pixel: Fill the 2x2 block with the input color
                output_grid[out_r, out_c] = input_color
                output_grid[out_r, out_c + 1] = input_color
                output_grid[out_r + 1, out_c] = input_color
                output_grid[out_r + 1, out_c + 1] = input_color
            else:
                # White pixel (0): Fill the 2x2 block with the specific pattern
                output_grid[out_r, out_c] = 1  # Blue
                output_grid[out_r, out_c + 1] = 0  # White
                output_grid[out_r + 1, out_c] = 0  # White
                output_grid[out_r + 1, out_c + 1] = 1  # Blue

    return output_grid
