"""
Create a new grid with the same height and double the width of the input grid.
The new grid is formed by placing the input grid next to a copy of itself.
The left part (columns 0 to width-1) is the original input, and the right part
(columns width to 2*width-1) is a copy of the original input.
"""

import numpy as np

def transform(input_grid):
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
                         Or potentially a numpy array if internal processing uses it.
                         Let's return a numpy array for consistency with potential
                         future complex operations, and the testing framework can
                         handle converting back if needed.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    # height, width = input_array.shape # not needed if using hstack

    # Horizontally stack the input array with itself
    # hstack takes a tuple of arrays to stack
    output_array = np.hstack((input_array, input_array))

    # The problem description implies list[list] might be expected,
    # but numpy arrays are standard for grid tasks. Returning array for now.
    # If list of lists is strictly required:
    # return output_array.tolist()
    return output_array
