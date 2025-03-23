"""
Rotate the input grid 90 degrees clockwise and then reverse the order of elements in each row.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Reverse the order of elements in each row (mirror horizontally)
    output_array = np.fliplr(rotated_array)

    # Convert the NumPy array back to a list
    output_grid = output_array.tolist()

    return output_grid