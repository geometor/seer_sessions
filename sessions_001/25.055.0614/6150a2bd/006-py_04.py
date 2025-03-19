"""
The output grid is obtained by first transposing the input grid (swapping rows and columns).
Then, reversing each row and each column of the *original* input and THEN transposing.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Reverse rows and columns
    reversed_array = input_array[::-1, ::-1]


    # Transpose the array (reflect across the main diagonal).
    output_array = reversed_array.T

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid