"""
The function takes a 2D grid of colored pixels as input, rotates it 90 degrees clockwise, and returns the rotated grid.  This is achieved by transposing the matrix such that row i becomes column (N-1-i).
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise by transposing such that row i of input
    becomes (N-1-i) column of output.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Get the dimensions of the input array.
    rows, cols = input_array.shape

    # Create an empty output array with swapped dimensions.
    output_array = np.empty((cols, rows), dtype=input_array.dtype)

    # Transpose the array such that row i becomes column (N-1-i)
    for i in range(rows):
        output_array[:, rows - 1 - i] = input_array[i, :]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid