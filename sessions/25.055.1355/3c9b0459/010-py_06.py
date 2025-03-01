"""
The input grid is rotated 90 degrees clockwise to produce the output grid. The dimensions of the grid are swapped (height becomes width, and width becomes height) during the rotation. Each pixel in the input grid maps to a new position in the output grid based on the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    output_array = np.rot90(input_array, k=-1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid