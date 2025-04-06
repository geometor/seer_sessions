"""
Transforms an input grid (represented as a NumPy array) by rotating it 180 degrees.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Rotates the input NumPy array grid by 180 degrees.

    Args:
        input_grid: A NumPy ndarray representing the input 2D integer grid.

    Returns:
        A NumPy ndarray representing the 180-degree rotated output grid.
    """
    # Apply a 180-degree rotation using numpy.rot90.
    # k=2 specifies two 90-degree counter-clockwise rotations, resulting in a 180-degree rotation.
    output_grid = np.rot90(input_grid, k=2)

    # Return the rotated grid
    return output_grid
