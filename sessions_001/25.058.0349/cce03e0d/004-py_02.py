"""
Expands the input grid by a factor of 3, preserving the original colors and their relative positions, and filling the adjacent cells to form a plus shape.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3

    # initialize output_grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid and map colors to the output grid
    for row in range(input_height):
        for col in range(input_width):
            # Calculate the corresponding position in the output grid
            output_row = row * 3
            output_col = col * 3

            # Copy the color value to the center of the 3x3 block
            output_grid[output_row + 1, output_col + 1] = input_grid[row, col]

            # Fill surrounding cells to create a plus shape
            output_grid[output_row, output_col + 1] = input_grid[row, col]  # Top
            output_grid[output_row + 2, output_col + 1] = input_grid[row, col]  # Bottom
            output_grid[output_row + 1, output_col] = input_grid[row, col]  # Left
            output_grid[output_row + 1, output_col + 2] = input_grid[row, col]  # Right

    return output_grid