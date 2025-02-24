"""
The transformation rule is: Keep all magenta (6) pixels, and set all other pixels to white (0). The shape of the grid remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by keeping magenta pixels and setting others to white.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Find all pixels that are NOT magenta (6).
    non_magenta_indices = np.where(output_grid != 6)

    # Set those non-magenta pixels to white (0).
    output_grid[non_magenta_indices] = 0

    return output_grid