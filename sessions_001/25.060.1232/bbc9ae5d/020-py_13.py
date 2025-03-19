"""
The transformation rule identifies the color of the top-left pixel and extends a rectangle of the same color. The contiguous block of pixels with the same color as the top-left pixel determines the height, and the input grid width determines the width. The height of the contiguous block will be the number of pixels in the first group of pixels of the same color starting from the top-left. Fill the rest with 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the top-left pixel's color.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    input_height, input_width = input_grid.shape
    initial_color = input_grid[0, 0]

    # Find the length of the contiguous block of the initial color.
    block_length = 0
    for x in range(input_width):
        if input_grid[0, x] == initial_color:
            block_length += 1
        else:
            break

    # Determine output dimensions.
    output_height = block_length
    output_width = input_width

    # Initialize the output grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill the rectangular region with the initial color.
    for y in range(output_height):
        for x in range(block_length):
            output_grid[y, x] = initial_color
    
    # The rest is already filled as 0 (white) because of initialization.

    return output_grid