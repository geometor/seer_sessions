"""
The transformation rule is to reverse the order of the rows of the input grid and then transpose the matrix (swap rows and columns). This is equivalent to a 180-degree rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing its rows and then transposing it.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows.
    reversed_rows = input_array[::-1]

    # Transpose the array (swap rows and columns).
    transposed_array = reversed_rows.T

    # Convert the result back to a list.
    output_grid = transposed_array.tolist()

    return output_grid