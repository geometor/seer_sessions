"""
Construct the output grid by horizontally concatenating the original input grid
with a horizontally reflected copy of the input grid. The resulting grid
will have the same height as the input and twice the width.
"""

import numpy as np

def transform(input_grid):
    """
    Takes an input grid (list of lists or numpy array), creates a horizontally
    reflected version, and concatenates the original and reflected grids
    side-by-side.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Create a horizontally reflected copy of the input array
    # Slicing [:, ::-1] reverses the order of columns
    reflected_array = input_array[:, ::-1]

    # Concatenate the original array and the reflected array horizontally
    # axis=1 specifies concatenation along the columns (horizontally)
    output_array = np.concatenate((input_array, reflected_array), axis=1)

    # Return the resulting output array
    return output_array
