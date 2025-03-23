"""
The function takes a 2D grid of colored pixels as input, rotates it 90 degrees clockwise, and returns the rotated grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    output_array = np.rot90(input_array, k=-1)  # k=-1 for clockwise rotation

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid