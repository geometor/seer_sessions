"""
Replaces all instances of blue (1) with grey (5) in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all blue pixels (1) with grey pixels (5).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all blue pixels (value 1).
    blue_pixels = np.where(output_grid == 1)

    # Replace the blue pixels with grey pixels (value 5).
    output_grid[blue_pixels] = 5

    return output_grid