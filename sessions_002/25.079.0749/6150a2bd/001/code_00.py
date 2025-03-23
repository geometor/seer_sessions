"""
The transformation rotates the input grid 90 degrees clockwise and then reverses the order of elements in each column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise
    rotated_grid = np.rot90(input_grid, k=-1)

    # Reverse each column in rotated_grid
    output_grid = np.flip(rotated_grid, axis=0)
    
    return output_grid.tolist()