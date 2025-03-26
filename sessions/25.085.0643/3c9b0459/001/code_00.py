"""
Rotates the input grid by 180 degrees to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: The grid rotated by 180 degrees.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    np_grid = np.array(input_grid, dtype=int)

    # Rotate the numpy array 180 degrees (equivalent to two 90-degree rotations)
    # k=2 specifies a 180-degree rotation (k=1 is 90, k=3 is 270)
    rotated_grid = np.rot90(np_grid, k=2)

    # Convert the rotated numpy array back to a list of lists
    output_grid = rotated_grid.tolist()

    return output_grid
