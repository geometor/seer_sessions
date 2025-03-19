"""
The transformation rule is: Find all pixels with the color blue (1) in the input grid. Change the color of these pixels to white (0). All other pixels in the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing all blue (1) pixels to white (0).

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is blue (1).
            if output_grid[i, j] == 1:
                # Change the pixel to white (0).
                output_grid[i, j] = 0

    return output_grid