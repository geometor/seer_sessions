"""
The transformation rule is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input list to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    #   1. Transpose the array (swap rows and columns).
    #   2. Reverse each row of the transposed array.  This achieves the 90-degree clockwise rotation.
    rotated_array = np.flip(input_array.T, axis=1)


    # Convert the NumPy array back to a list.
    output_grid = rotated_array.tolist()

    return output_grid