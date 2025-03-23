"""
The transformation maps the input grid coordinates to the output grid coordinates as follows:

1.  The input grid's rows become the output grid's columns *in reversed order*.
2.  The input grid's columns become the output grid's rows *in reversed order*.

Mathematically:
  input (r, c) -> output (C - 1 - c, R - 1 - r)
Where R is the number of rows and C is the number of columns in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting across both axes (180-degree rotation).
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)
    rows = input_array.shape[0]
    cols = input_array.shape[1]

    # Initialize the output array with zeros.
    output_array = np.zeros_like(input_array)

    # Map input coordinates to output coordinates.
    for r in range(rows):
        for c in range(cols):
            new_r = cols - 1 - c
            new_c = rows - 1 - r
            output_array[new_r, new_c] = input_array[r, c]

    # Convert the output array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid