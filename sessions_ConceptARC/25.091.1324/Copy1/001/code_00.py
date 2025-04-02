"""
Transforms an input grid by horizontally concatenating it with itself.
The output grid has the same height as the input grid and twice the width.
The left half of the output grid is identical to the input grid, and the right half is also identical to the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Horizontally concatenates the input grid with itself.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid, which is the input grid
        concatenated horizontally with itself.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Concatenate the input array with itself horizontally (along axis 1)
    # The first argument is a tuple containing the arrays to concatenate
    # The second argument specifies the axis along which to concatenate (1 for columns)
    output_grid = np.concatenate((input_array, input_array), axis=1)

    # Return the resulting concatenated grid
    return output_grid
