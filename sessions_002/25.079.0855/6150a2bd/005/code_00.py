"""
The input grid is rotated 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    rotated_array = np.rot90(input_array, k=-1)

    # Convert the rotated array back to a list.
    output_grid = rotated_array.tolist()

    return output_grid