"""
The input is a single-row grid containing a single non-zero pixel. The output is a square grid.
The size (width and height) of the output grid is determined by the value of the non-zero pixel
in the input grid.  If the input pixel's value is 'n', the output grid will be 'n x n'.
The output grid contains a diagonal line of pixels, all of which have the same color as the
non-zero pixel in the input. This diagonal runs from the top-right corner to the bottom-left
corner of the square grid. All other pixels in the output grid are black (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid (single-row) into a square output grid with a diagonal.

    Args:
        input_grid: A 2D numpy array representing the input grid (single row).

    Returns:
        A 2D numpy array representing the square output grid.
    """
    # Find the non-zero pixel and its value.
    non_zero_indices = np.nonzero(input_grid)
    if len(non_zero_indices[0]) == 0:
        return input_grid.copy()  # Return input if no non-zero pixel

    non_zero_value = input_grid[non_zero_indices[0][0], non_zero_indices[1][0]]

    # Determine the size of the output grid.
    grid_size = non_zero_value

    # Create an output grid filled with zeros.
    output_grid = np.zeros((grid_size, grid_size), dtype=int)

    # Fill the diagonal with the non-zero element.
    for i in range(grid_size):
        output_grid[i, grid_size - 1 - i] = non_zero_value

    return output_grid