"""
The transformation rule is a reflection of the grid across the main diagonal (top-left to bottom-right).
This is equivalent to transposing the matrix.
"""

import numpy as np

def transform(input_grid):
    """
    Reflects the input grid across its main diagonal (transposes the matrix).
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array.
    output_array = input_array.T

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid