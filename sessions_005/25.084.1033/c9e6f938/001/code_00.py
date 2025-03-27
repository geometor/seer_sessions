"""
Horizontally reflect the input grid and append the reflection to the right of the original input. The output grid's height matches the input's height, and the output width is double the input's width. The left half of the output is identical to the input, and the right half is a horizontal mirror image of the input.
"""

import numpy as np

def transform(input_grid):
    """
    Takes an input grid, creates a horizontally reflected copy, and concatenates
    the original and the reflected copy side-by-side.

    Args:
        input_grid (list or np.array): The input grid (2D array of integers).

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_np.shape

    # Create the output grid with double the width
    # Initialize with zeros or any default value, though it will be overwritten
    output_width = 2 * width
    output_grid = np.zeros((height, output_width), dtype=int)

    # Copy the original input grid to the left half of the output grid
    # Slicing: output_grid[rows, columns]
    output_grid[:, 0:width] = input_np

    # Create a horizontally flipped version of the input grid
    flipped_input = np.fliplr(input_np)

    # Copy the flipped input grid to the right half of the output grid
    output_grid[:, width:output_width] = flipped_input

    return output_grid
