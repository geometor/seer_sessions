"""
The transformation rule involves transposing the input grid.
The rows of the input grid become the columns of the output grid, and vice-versa.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array.  Rows become columns, and columns become rows.
    output_array = input_array.T

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid