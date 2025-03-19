"""
The output grid retains only the pixels that were originally maroon (color 9) in the input grid. All other pixels are removed (become implicitly color 0, or white/blank, as they are not present in the output). The output grid dimensions match the input dimensions, and only consists of the pixels that were color 9 in the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid, keeping only the pixels that were originally maroon (9).

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the output grid.
    """
    # Create an output grid of the same shape as the input, initialized with 0s (white).
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid and copy only the maroon pixels to the output grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 9:
                output_grid[i, j] = 9

    return output_grid