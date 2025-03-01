"""
The transformation rule is to replace all magenta (6) pixels with grey (5) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all magenta (6) pixels with grey (5) pixels.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find all pixels with the value 6 (magenta) and change them to 5 (grey).
    output_grid[output_grid == 6] = 5

    return output_grid