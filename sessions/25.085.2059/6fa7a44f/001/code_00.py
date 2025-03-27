"""
Vertically mirrors the input grid and appends the mirrored version below the original input grid.
The output grid's height is double the input grid's height, while the width remains the same.
The top half of the output grid is identical to the input grid.
The bottom half of the output grid is the input grid flipped vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking it on top of its vertical reflection.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_np.shape

    # Create the output grid with double the height and the same width
    output_height = height * 2
    output_grid = np.zeros((output_height, width), dtype=int)

    # Copy the input grid to the top half of the output grid
    output_grid[0:height, :] = input_np

    # Create a vertically flipped version of the input grid
    # Slicing [::-1] reverses the order of rows
    flipped_input = input_np[::-1, :]

    # Copy the flipped input grid to the bottom half of the output grid
    output_grid[height:output_height, :] = flipped_input

    # Return the final output grid
    return output_grid
