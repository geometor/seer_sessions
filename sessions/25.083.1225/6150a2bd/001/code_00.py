"""
1. Rotate: Rotate the entire input grid clockwise by 90 degrees.
2. Reverse row order: Reverse the order of the rows in the rotated grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise and then
    reversing the order of the rows.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    rotated_array = np.rot90(input_array, k=-1)

    # Reverse the order of the rows.
    output_array = np.flipud(rotated_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid