"""
Iterate through each pixel in the input grid.  If the pixel's value is 5, 6,
or 8 change the pixel's value by adding 4 and taking the modulus of 10.
Otherwise, leave the pixel's value unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the observed rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate over each cell in the grid
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # If the pixel's value is 5, 6, or 8, apply the transformation
            if output_grid[row_index, col_index] in (5, 6, 8):
                output_grid[row_index, col_index] = (output_grid[row_index, col_index] + 4) % 10
            # Otherwise, the pixel's value is unchanged.

    return output_grid