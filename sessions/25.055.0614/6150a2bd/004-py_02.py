"""
The input grid is reflected across the main diagonal (top-left to bottom-right).  This is equivalent to a transposition operation where the rows and columns are swapped.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array (reflect across the main diagonal).
    output_array = input_array.T

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid