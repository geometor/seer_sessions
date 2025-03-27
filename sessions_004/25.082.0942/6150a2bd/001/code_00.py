"""
The input grid is transformed to the output grid by transposing (swapping rows and columns) and then rotating it 90 degrees counter-clockwise.
This is equivalent to reversing the order of the rows of the transposed grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it and reversing its rows.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array (swap rows and columns).
    transposed_array = input_array.T

    # Reverse the order of rows in the transposed array.
    output_array = np.flip(transposed_array, axis=0)
    
    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid