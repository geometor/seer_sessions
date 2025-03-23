"""
The input grid is rotated 90 degrees counter-clockwise to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    rotated_array = np.rot90(input_array, k=1)

    # Convert the rotated array back to a list of lists.
    output_grid = rotated_array.tolist()

    return output_grid