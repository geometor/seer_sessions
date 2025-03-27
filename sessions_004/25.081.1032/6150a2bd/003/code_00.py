"""
The transformation rule involves reversing the order of the columns of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its columns.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with reversed columns.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of columns in the array.
    output_array = np.flip(input_array, axis=1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid