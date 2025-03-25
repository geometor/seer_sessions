"""
The transformation removes all even-numbered rows (starting with the top row as index 0) and removes all columns which contains only zeroes, then packs the remaining elements into a smaller grid. The relative horizontal positions of the non-zero elements are preserved.
"""

import numpy as np

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Identify columns that contain at least one non-zero value
    non_zero_cols = []
    for j in range(input_array.shape[1]):
        if np.any(input_array[:, j] != 0):
            non_zero_cols.append(j)
    
    # Filter input array to only keep non-zero columns
    filtered_array = input_array[:, non_zero_cols]

    # Select only odd-numbered rows (starting from index 0).
    output_array = filtered_array[::2]

    # Convert back to list for the required output format.
    output_grid = output_array.tolist()

    return output_grid