"""
The input grid is rotated -90 degrees (270 degrees clockwise).
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by -90 degrees.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the rotated grid.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array by -90 degrees (equivalent to 270 degrees clockwise)
    rotated_array = np.rot90(input_array, k=-1)

    # Convert the rotated array back to a list
    output_grid = rotated_array.tolist()

    return output_grid