"""
The input grid is rotated 90 degrees counter-clockwise to create the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees counter-clockwise.

    Args:
    input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
    list of lists: The rotated grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    rows = input_array.shape[0]
    cols = input_array.shape[1]

    # Create an empty output array with swapped dimensions
    output_array = np.empty((cols, rows), dtype=input_array.dtype)

    # Rotate the array 90 degrees counter-clockwise
    for i in range(rows):
        for j in range(cols):
            output_array[j, rows - 1 - i] = input_array[i, j]


    # Convert the rotated array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid