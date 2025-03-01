"""
Identify blue objects and transform them into green objects while keeping other objects unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing blue pixels to green.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through the grid and change blue (1) pixels to green (3).
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 1:
                output_grid[i, j] = 3

    return output_grid