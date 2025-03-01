"""
The transformation rule is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D list or numpy array representing the rotated output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    output_array = np.rot90(input_array, k=-1)

    # Convert back to list (if desired, otherwise return the numpy array)
    output_grid = output_array.tolist()

    return output_grid