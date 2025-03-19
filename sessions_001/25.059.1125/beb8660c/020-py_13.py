"""
The input grid is rotated 90 degrees clockwise. The diagonal line is not a consistent feature and should be ignored.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)  # k=-1 for 90 degrees clockwise

    # Convert the rotated array back to a list and return
    return rotated_array.tolist()