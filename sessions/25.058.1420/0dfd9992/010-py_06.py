"""
The transformation rule removes all white pixels (value 0) from the input grid. The remaining non-white pixels are compacted downwards within their original columns. The output is a single column wide and only has non-white pixels.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    num_rows, num_cols = input_grid.shape
    
    # Create a list to store the compacted non-white pixels.
    compacted_pixels = []

    # Iterate through each column of the input grid.
    for j in range(num_cols):
        # Extract the current column.
        column = input_grid[:, j]

        # Filter out the white pixels (value 0) from the column.
        non_white_pixels = column[column != 0]

        # Add the non-white pixels to the compacted_pixels list.
        compacted_pixels.extend(non_white_pixels)

    # Convert the list of compacted pixels to a NumPy array and reshape it
    # to have a single column.
    output_grid = np.array(compacted_pixels).reshape(-1, 1)

    return output_grid