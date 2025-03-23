"""
The input grid is reflected across both its horizontal and vertical axes. This is equivalent to reversing the order of rows and then reversing the order of elements within each row, or vice-versa.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it across both horizontal and vertical axes.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows.
    reversed_rows = input_array[::-1]

    # Reverse the order of elements within each row.
    output_array = np.flip(reversed_rows, axis=1)
    #output_array = reversed_rows[:, ::-1] # alternative using slicing


    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid