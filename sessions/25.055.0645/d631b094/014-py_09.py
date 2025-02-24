"""
Find the non-zero value in the input grid and return a 1x1 grid containing that value.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find the indices of the non-zero elements.
    non_zero_indices = np.nonzero(input_array)

    # Extract the non-zero value.  We assume there's only one.
    non_zero_value = input_array[non_zero_indices[0][0], non_zero_indices[1][0]]

    # Create a 1x1 output grid containing the non-zero value.
    output_grid = np.array([[non_zero_value]])

    return output_grid