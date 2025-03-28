"""
Transforms an input grid into an output grid twice the height and width.
Each pixel in the input grid maps to a 2x2 block in the output grid.
If the input pixel color is non-white (C > 0), the corresponding 2x2 output block is filled entirely with color C.
If the input pixel color is white (C = 0), the corresponding 2x2 output block is filled with the pattern [[1, 0], [0, 1]] (blue, white / white, blue).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid (e.g., with zeros/white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define the replacement pattern for white input pixels
    white_replacement_pattern = np.array([[1, 0], [0, 1]], dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_grid[r, c]

            # Calculate the top-left coordinates for the 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2

            # Apply the transformation based on the input pixel color
            if input_color > 0:
                # Fill the 2x2 block with the input color
                output_grid[out_r:out_r+2, out_c:out_c+2] = input_color
            else: # input_color == 0 (white)
                # Fill the 2x2 block with the specific pattern
                output_grid[out_r:out_r+2, out_c:out_c+2] = white_replacement_pattern

    return output_grid