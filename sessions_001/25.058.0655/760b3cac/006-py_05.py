"""
1. Copy: All yellow pixels from the input grid are copied to the output grid without any changes.
2. Shift Azure (Top 3 Rows): Azure pixels within the top three rows (0, 1, and 2) of the input grid are shifted horizontally. The amount and direction of the shift is determined by the horizontal distance to the leftmost azure pixel within the same row.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy yellow pixels directly.
    # No change needed as we are copying the whole input_grid

    # 2. Transform azure pixels in the top 3 rows.
    for row_index in range(min(3, rows)):  # Iterate through the top 3 rows
        # Find the leftmost azure pixel's column in the current row
        leftmost_col = cols
        azure_pixels = []
        for c in range(cols):
            if input_grid[row_index, c] == 8:
                leftmost_col = min(leftmost_col, c)
                azure_pixels.append((row_index, c))

        # Shift azure pixels in the current row if any exist
        if azure_pixels:
            for r, c in azure_pixels:
                output_grid[r, c] = 0  # Clear original position
                new_c = c - leftmost_col
                output_grid[r, new_c] = 8  # Set new position


    return output_grid