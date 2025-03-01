"""
The transformation rule is to replace all pixels of color 5 with color 0, and keep all other pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all instances of color 5 with color 0.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Replace all instances of color 5 with color 0.
    output_grid[output_grid == 5] = 0

    return output_grid