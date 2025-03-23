"""
The transformation rule is a matrix transposition. The input grid is transposed to create the output grid. Specifically, the element at `input[row][column]` is moved to `output[column][row]` for all rows and columns. The digits do not change, it is their position in the array that changes.
"""

import numpy as np

def transform(input_grid):
    """
    Transposes the input grid.
    """
    # Convert the input grid to a NumPy array.  This makes transposition easy.
    input_array = np.array(input_grid)

    # Transpose the array.  The .T attribute gives the transpose.
    output_array = input_array.T

    # Convert the transposed array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid