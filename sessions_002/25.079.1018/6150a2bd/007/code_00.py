"""
The transformation rule consists of a 90-degree clockwise rotation of the input grid, followed by a horizontal flip (reflection across the vertical axis).
"""

import numpy as np

def transform(input_grid):
    """
    Applies a 90-degree clockwise rotation followed by a horizontal flip to the input grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise (k=-1 for clockwise).
    rotated_array = np.rot90(input_array, k=-1)

    # Flip the rotated array horizontally.
    flipped_array = np.fliplr(rotated_array)

    # Convert the transformed array back to a list of lists.
    output_grid = flipped_array.tolist()

    return output_grid