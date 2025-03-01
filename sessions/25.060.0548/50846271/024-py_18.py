"""
Identify red (2) pixels in the input grid. Replace the leftmost red pixels in each row with azure (8) pixels. The rest of the grid (gray (5) and white (0) pixels) remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing the leftmost red pixels in each row with azure pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each row.
    for row_index in range(output_grid.shape[0]):
        # Find red pixels in the current row.
        row = output_grid[row_index]
        red_indices = np.where(row == 2)[0]


        # If there are red pixels in the row, find the leftmost one.
        if len(red_indices) > 0:
            leftmost_red_index = red_indices[0]

            # Replace the leftmost red pixel with azure.
            output_grid[row_index, leftmost_red_index] = 8

    return output_grid