"""
The input grid is rotated 90 degrees clockwise. The color of each pixel in the input grid is preserved in its new position in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    output_array = np.rot90(input_array, k=-1)

    # Convert the rotated array back to a list.
    output_grid = output_array.tolist()

    return output_grid