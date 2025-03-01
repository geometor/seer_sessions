"""
Iterates through each row of the input grid. If a row contains any azure (color code 8) pixels,
it changes all pixels in that entire row to azure. Rows without azure are left unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each row
    for row_index in range(output_grid.shape[0]):
        # Check if the row contains any azure pixels
        if np.any(output_grid[row_index] == 8):
            # Fill the entire row with azure
            output_grid[row_index, :] = 8

    return output_grid