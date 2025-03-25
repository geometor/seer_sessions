"""
Expands each pixel in the input grid into a 2x2 square of the same color in the output grid, effectively doubling the dimensions of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each pixel into a 2x2 block.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Iterate through each cell of the input grid
    for row in range(input_height):
        for col in range(input_width):
            pixel_value = input_grid[row][col]
            # Expand the pixel to a 2x2 block in the output grid
            output_grid[row * 2][col * 2] = pixel_value
            output_grid[row * 2 + 1][col * 2] = pixel_value
            output_grid[row * 2][col * 2 + 1] = pixel_value
            output_grid[row * 2 + 1][col * 2 + 1] = pixel_value

    return output_grid