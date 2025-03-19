"""
The function rotates a 3x3 grid 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the rotated grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array (swap rows and columns).
    transposed_array = input_array.T

    # Reverse each row of the transposed array to achieve a 90-degree clockwise rotation.
    rotated_array = np.flip(transposed_array, axis=1)

    # Convert the NumPy array back to a list of lists.
    output_grid = rotated_array.tolist()

    return output_grid