"""
The input grid is rotated counter-clockwise by 90 degrees.
Alternatively, read input grid diagonally from bottom-left to top-right,
and write to output grid diagonally from top-right to bottom-left.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it counter-clockwise by 90 degrees.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array counter-clockwise by 90 degrees.  The numpy 'rot90'
    # function rotates by default in the counter-clockwise direction.
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid