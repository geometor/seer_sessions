"""
The transformation extracts the non-zero pixels from the input grid, 
creating the output grid's dimensions by multiplying the length of the 
unique values by their repetition.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Identify non-zero pixels.
    non_zero_pixels = input_array[input_array != 0]

    # Count occurrences of each unique non-zero value.
    unique_values, counts = np.unique(non_zero_pixels, return_counts=True)
    
    # Determine the total size of the output array
    total_size = np.sum(counts)
    
    # construct output array
    output_array = np.repeat(unique_values, counts)

    return output_array.tolist()