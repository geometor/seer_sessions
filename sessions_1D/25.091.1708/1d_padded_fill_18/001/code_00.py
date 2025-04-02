"""
For each row in the input grid:
1. Identify if any non-white pixels exist in the row.
2. If non-white pixels exist:
    a. Determine the color (C) of these pixels (assuming they are all the same color within a row).
    b. Find the column index of the leftmost non-white pixel (min_col).
    c. Find the column index of the rightmost non-white pixel (max_col).
    d. Fill the segment of the row in the output grid from min_col to max_col (inclusive) with color C.
3. If no non-white pixels exist, the row remains unchanged.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal segment between the leftmost and rightmost non-white pixels
    in each row with the color of those pixels.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row = input_grid[r, :]
        # Find the indices of non-white pixels (color != 0)
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if len(non_white_indices) > 0:
            # Find the minimum and maximum column indices of non-white pixels
            min_col = np.min(non_white_indices)
            max_col = np.max(non_white_indices)

            # Get the color from the first non-white pixel found in this row
            # Assumes all non-white pixels in a relevant row have the same color
            fill_color = row[min_col]

            # Fill the segment in the output grid row
            output_grid[r, min_col : max_col + 1] = fill_color

    return output_grid