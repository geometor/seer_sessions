"""
Identify all pixels with the color gray (5) in the input grid.
Change these gray pixels to yellow (4) in the output grid.
All other pixels remain the same color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing gray (5) pixels with yellow (4).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The output grid with gray pixels replaced by yellow.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Find the indices of all gray pixels (value 5).
    gray_indices = np.where(output_grid == 5)

    # Replace the gray pixels with yellow (value 4).
    output_grid[gray_indices] = 4

    return output_grid