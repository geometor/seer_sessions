"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid.
2.  **Row-wise Iteration:** Process each row of the input grid independently.
3.  **Pixel Examination:** For each pixel in the current row:
    *   If the pixel is white (0), keep its value unchanged in the output grid.
    *   If the pixel is azure (8):
        *   Maintain a counter for azure pixels encountered in the *current row*.
        *   If the current row index is even:
            *   If the azure pixel count is even, replace it with red (2).
            *   If the azure pixel count is odd, replace it with gray (5).
        *   If the current row index is odd:
            *   If the azure pixel count is even, replace it with gray (5).
            *   If the azure pixel count is odd, replace it with red (2).
        *   Increment the azure pixel counter for the current row.
4.  **Output:** Return the transformed output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
        eight_count = 0  # Counter for '8's in the current row
        for j in range(cols):
            # Preserve '0'
            if input_grid[i, j] == 0:
                continue  # Do nothing, keep '0' as is
            # Conditional Substitution for '8'
            elif input_grid[i, j] == 8:
                # Determine color based on row parity and eight_count
                if i % 2 == 0:  # Even row
                    if eight_count % 2 == 0:
                        output_grid[i, j] = 2  # Red
                    else:
                        output_grid[i, j] = 5  # Gray
                else:  # Odd row
                    if eight_count % 2 == 0:
                        output_grid[i, j] = 5  # Gray
                    else:
                        output_grid[i, j] = 2  # Red
                eight_count += 1  # Increment the '8' counter for the current row

    return output_grid