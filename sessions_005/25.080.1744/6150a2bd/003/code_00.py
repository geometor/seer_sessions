"""
Rotate the input grid 90 degrees counter-clockwise.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the input array 90 degrees counter-clockwise.
    rotated_array = np.rot90(input_array, k=1)

    # Convert the rotated array back to a list.
    output_grid = rotated_array.tolist()

    return output_grid