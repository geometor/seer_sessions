"""
Replace all instances of '6' with '2'. Leave '7' unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all '6's with '2's, leaving '7's unchanged.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the cell value is 6, change it to 2.
            if output_grid[i, j] == 6:
                output_grid[i, j] = 2

    return output_grid