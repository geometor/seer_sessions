"""
1. Rotate the entire input grid 90 degrees clockwise.
2. Mirror the entire rotated grid across it's horizontal axis
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    rotated_array = np.rot90(input_array, k=-1)  # k=-1 for clockwise rotation

    # Mirror the rotated array horizontally
    mirrored_array = np.flip(rotated_array, axis=0) # flip across the horizontal axis

    # Convert the NumPy array back to a list of lists.
    output_grid = mirrored_array.tolist()

    return output_grid