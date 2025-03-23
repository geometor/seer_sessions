"""
The transformation rule is to transpose the input grid, swapping rows and columns. 
The element at input[row][col] moves to output[col][row].
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array.
    output_array = input_array.T

    # Convert the transposed array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid