"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the rotated grid.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Use NumPy's rot90 function to perform the rotation.
    rotated_array = np.rot90(input_array)

    # Convert the result back to a list.
    output_grid = rotated_array.tolist()

    return output_grid