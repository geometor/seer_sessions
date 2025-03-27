"""
Transforms an input grid by scaling it by a factor of 2. Each pixel in the input grid maps to a 2x2 block in the output grid. If the input pixel is white (0), the output block is all white (0). If the input pixel is gray (5), the output block follows the pattern [[blue(1), red(2)], [red(2), blue(1)]].
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid (double the input)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_grid[r, c]

            # Determine the top-left coordinates for the 2x2 block in the output grid
            out_r_start = r * 2
            out_c_start = c * 2

            # Apply the mapping rule based on the input color
            if input_color == 5:  # Gray maps to the specific pattern
                output_grid[out_r_start,     out_c_start]     = 1 # blue
                output_grid[out_r_start,     out_c_start + 1] = 2 # red
                output_grid[out_r_start + 1, out_c_start]     = 2 # red
                output_grid[out_r_start + 1, out_c_start + 1] = 1 # blue
            # No explicit action needed for input_color == 0 (white),
            # as the output grid is already initialized with 0s.

    return output_grid