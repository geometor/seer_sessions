"""
Extracts the non-zero color from the input grid, counts its occurrences, and creates a 1-dimensional array of that color with a length equal to the count.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find the non-zero color in the input grid.
    non_zero_values = input_array[input_array != 0]
    if non_zero_values.size == 0:  # Handle the case where there are no non-zero values
       return [] # return empty array
    
    non_zero_color = non_zero_values[0]

    # Count the occurrences of the non-zero color.
    count = np.count_nonzero(input_array == non_zero_color)

    # Create an output grid (1D array) filled with the non-zero color.
    output_grid = np.full((1, count), non_zero_color)

    return output_grid.tolist()