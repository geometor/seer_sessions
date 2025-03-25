"""
The transformation rule is a reflection of the input grid across its main diagonal. In other words, the pixel at input position (row, col) moves to output position (col, row). This is equivalent to a matrix transposition.
"""

import numpy as np

def transform(input_grid):
    """
    Transposes the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transposed output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array.
    output_array = np.transpose(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid