"""
Extract the left half of the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Determine the number of columns in the input grid
    num_cols = input_array.shape[1]

    # Calculate the output width (number of columns to keep)
    output_width = num_cols // 2

    # Crop the input array to create the output array
    output_array = input_array[:, :output_width]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid