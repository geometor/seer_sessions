"""
Rotate the input grid 180 degrees.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 180 degrees.
    rotated_array = np.rot90(input_array, k=2)  # k=2 for 180-degree rotation

    # Convert the NumPy array back to a list of lists.
    output_grid = rotated_array.tolist()

    return output_grid