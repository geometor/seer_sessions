"""
Transforms an input grid into an output grid of double the dimensions.
Each pixel in the input grid maps to a 2x2 block in the output grid.
If the input pixel color is non-white (not 0), the corresponding 2x2 output block is filled with that color.
If the input pixel color is white (0), the corresponding 2x2 output block is filled with a pattern: white (0) on the main diagonal and blue (1) on the anti-diagonal.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]
            
            # Define the top-left corner of the 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2

            # Apply transformation based on input pixel color
            if input_color != 0:
                # Fill the 2x2 block with the input color
                output_grid[out_r:out_r+2, out_c:out_c+2] = input_color
            else:
                # Fill the 2x2 block with the white/blue pattern
                output_grid[out_r, out_c] = 0  # Top-left (white)
                output_grid[out_r, out_c + 1] = 1  # Top-right (blue)
                output_grid[out_r + 1, out_c] = 1  # Bottom-left (blue)
                output_grid[out_r + 1, out_c + 1] = 0  # Bottom-right (white)

    # Convert back to list of lists if necessary, although numpy array is often preferred
    return output_grid.tolist()
