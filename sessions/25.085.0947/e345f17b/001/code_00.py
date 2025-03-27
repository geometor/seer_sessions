"""
Generates an output grid by comparing corresponding pixels from the left and right halves of the input grid.
The output grid has the same height as the input but half the width.
A pixel in the output grid at (row, col) is set to yellow (4) if and only if
the input grid pixels at (row, col) AND (row, col + half_width) are both white (0).
Otherwise, the output pixel is set to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the rule described above.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid
    output_height = input_height
    output_width = input_width // 2 # Output width is half the input width

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixel values from the left and right halves of the input grid
            left_pixel_value = input_grid[r, c]
            right_pixel_value = input_grid[r, c + output_width] # c + output_width gives the column index in the right half

            # Check the condition: if both corresponding input pixels are white (0)
            if left_pixel_value == 0 and right_pixel_value == 0:
                # Set the output pixel to yellow (4)
                output_grid[r, c] = 4
            # Otherwise, the output pixel remains white (0) as initialized

    return output_grid