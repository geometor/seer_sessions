"""
The input grid is rotated 90 degrees clockwise to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the rotated output grid.
    """
    # Convert the input list of lists to a NumPy array
    input_grid = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize the output grid with swapped dimensions
    output_grid = np.zeros((cols, rows), dtype=input_grid.dtype)

    # Rotate the grid 90 degrees clockwise
    for i in range(rows):
        for j in range(cols):
            output_grid[j, rows - 1 - i] = input_grid[i, j]

    return output_grid.tolist()