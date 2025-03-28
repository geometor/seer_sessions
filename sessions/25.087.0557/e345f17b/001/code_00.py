"""
Compares corresponding pixels from the left and right halves of the input grid.
If both the pixel in the left half at (r, c) and the pixel in the right half
at (r, c + width/2) are white (0), the output pixel at (r, c) becomes yellow (4).
Otherwise, the output pixel is white (0). The output grid has the same height
as the input but half the width.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on pixel comparison between its left and right halves.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height
    output_width = input_width // 2 # Integer division for width

    # Initialize the output grid with white (0)
    # This handles the 'else' condition by default
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell corresponding to the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixels from the left and right halves of the input grid
            left_pixel = input_grid[r, c]
            right_pixel = input_grid[r, c + output_width] # Add output_width offset for right half

            # Apply the transformation rule
            if left_pixel == 0 and right_pixel == 0:
                output_grid[r, c] = 4 # Set to yellow if both corresponding inputs are white

    return output_grid
