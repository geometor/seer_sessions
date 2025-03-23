"""
The transformation rule is to rotate the input grid by 180 degrees to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees (two 90-degree rotations)
    rotated_array = np.rot90(input_array, 2)

    # Convert the rotated array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid