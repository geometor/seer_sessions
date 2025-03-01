"""
Replace all azure pixels with gray pixels, leaving all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing azure (8) pixels with gray (5) pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find all azure pixels (value 8) and replace them with gray (value 5).
    output_grid[output_grid == 8] = 5

    return output_grid