"""
Rotate the input grid by 180 degrees to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The grid rotated by 180 degrees.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Rotate the numpy array 180 degrees (equivalent to two 90-degree rotations)
    # np.rot90 rotates counterclockwise, so k=2 is 180 degrees.
    output_grid = np.rot90(input_np, k=2)

    return output_grid
