"""
Find the smallest non-zero value in the input grid and return a 1x1 grid containing that value.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)

    # Find the indices of the non-zero elements.
    non_zero_indices = np.nonzero(input_array)

    # Get the non-zero values.
    non_zero_values = input_array[non_zero_indices]

    # Find the minimum non-zero value.
    if non_zero_values.size > 0:
        min_non_zero_value = np.min(non_zero_values)
    else:
        min_non_zero_value = 0 #should not happen based on problem, but handle anyway

    # Create a 1x1 output grid containing the minimum non-zero value.
    output_grid = np.array([[min_non_zero_value]])

    return output_grid