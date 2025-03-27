"""
Transforms an input grid by replacing all pixels with the color orange (value 7) 
with the color gray (value 5). All other pixel colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Replaces all orange pixels (7) with gray pixels (5).

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A new 2D numpy array with orange pixels replaced by gray.
    """
    # Create a copy of the input grid to modify.
    # This ensures the original input grid is not changed.
    output_grid = np.copy(input_grid)

    # Find the locations (indices) of all pixels with the value 7 (orange).
    orange_pixels = (output_grid == 7)

    # Change the color of the identified orange pixels to 5 (gray) in the output grid.
    output_grid[orange_pixels] = 5

    # Return the modified grid.
    return output_grid