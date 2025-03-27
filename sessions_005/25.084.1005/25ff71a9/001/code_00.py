"""
Shifts the entire content of the input grid down by one row.
The top row of the output grid is filled with the background color (white, 0).
The content from the last row of the input grid is discarded.
"""

import numpy as np

def transform(input_grid):
    """
    Shifts the grid content down by one row, filling the top row with white (0).

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the background color (0)
    # Using np.zeros creates an array filled with 0s, which is the background color.
    output_grid = np.zeros((height, width), dtype=int)

    # Shift the content down
    # Iterate through the rows of the input grid, excluding the last row
    # because its content will be shifted off the grid.
    # The range goes up to height - 1 for the input row index.
    # The corresponding output row index will be input_row_index + 1.
    if height > 1:
        # Copy rows from input[0] to input[height-2]
        # to output[1] to output[height-1]
        output_grid[1:height, :] = input_np[0:height-1, :]

    # The first row (index 0) of the output_grid is already filled with 0s
    # due to np.zeros initialization. No explicit filling step is needed.

    return output_grid.tolist() # Convert back to list of lists if required by ARC framework
