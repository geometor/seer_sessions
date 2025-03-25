"""
Replaces all instances of '5' in the input grid with a sequence of numbers starting from 1, proceeding in column-major order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing 5s with a sequence of numbers.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    replacement_sequence = 1

    # Iterate through columns
    for j in range(output_grid.shape[1]):
        # Iterate through rows within each column
        for i in range(output_grid.shape[0]):
            # Check if the cell value is 5
            if output_grid[i, j] == 5:
                # Replace the cell value with the current sequence value
                output_grid[i, j] = replacement_sequence
                # Increment the sequence value
                replacement_sequence += 1

    return output_grid