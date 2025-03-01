"""
The input grid is mirrored along the diagonal axis extending from the top-right corner to the bottom-left corner.
Colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring it along the top-right to bottom-left diagonal.
    Colors are left unchanged

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate over the input grid and mirror the pixels.
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = input_grid[j, i]

    # swap to correct orientation
    output_grid = np.fliplr(output_grid)
            
    return output_grid