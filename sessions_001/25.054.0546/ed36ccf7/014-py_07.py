"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid. Pixels maintain their values, but their positions change according to the rotation.
"""

import numpy as np

def transform(input_grid):
    """Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The rotated output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the rotated array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid