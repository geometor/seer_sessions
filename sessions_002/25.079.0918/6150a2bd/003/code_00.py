"""
The transformation rule involves two steps:
1. Transpose the matrix (swap rows and columns).
2. Reverse the order of the rows in the transposed matrix.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it and then reversing the rows
    of the transposed matrix.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array (swap rows and columns).
    transposed_array = input_array.T

    # Reverse the order of rows in the transposed array.
    reversed_rows_array = transposed_array[::-1]

    # Convert the result back to a list.
    output_grid = reversed_rows_array.tolist()

    return output_grid