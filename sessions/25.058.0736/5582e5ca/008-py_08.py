"""
The transformation rule is to replace all pixels in the input grid with the color maroon (value 9), regardless of their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all pixels with the color maroon (value 9).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid with the same shape as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace all pixel values in output with 9
    for i in range(rows):
       for j in range(cols):
          output_grid[i,j] = 9

    return output_grid