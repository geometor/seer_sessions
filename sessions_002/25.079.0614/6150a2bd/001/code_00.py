"""
Reverse the order of the rows and then transpose the matrix.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its rows and then transposing it.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """

    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # 1. Reverse the order of rows.
    reversed_rows_array = input_array[::-1]

    # 2. Transpose the array (swap rows and columns).
    transposed_array = reversed_rows_array.T

    # Convert the result back to a list of lists.
    output_grid = transposed_array.tolist()

    return output_grid