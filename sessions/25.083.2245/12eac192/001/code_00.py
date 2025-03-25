"""
Iterate through each cell of the input grid. If a cell's value is 1 (blue), 
change it to 3 (green) in the output grid. Otherwise, keep the original value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all occurrences of 1 with 3.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Iterate over all cells using indices.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the cell value is 1.
            if output_grid[i, j] == 1:
                # Replace 1 with 3.
                output_grid[i, j] = 3

    return output_grid