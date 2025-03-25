"""
For each column, find the lowest yellow pixel (excluding the bottom row). Fill all pixels above it (up to row 0) with yellow, creating a solid rectangular block. Leave other pixels as is. The bottom row of the output is identical to the input.
"""

import numpy as np

def get_yellow_pixels(grid):
    """
    Finds coordinates of all yellow pixels in the grid.
    """
    yellow_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 4:
                yellow_pixels.append((row_idx, col_idx))
    return yellow_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through columns
    for col in range(cols):
        # Get yellow pixel row indices in the current column (excluding the bottom row)
        yellow_rows = [row for row, c in get_yellow_pixels(input_grid) if c == col and row != rows - 1]

        # If there are yellow pixels in the column (excluding the bottom row)
        if yellow_rows:
            # Find the lowest yellow pixel's row index (excluding the bottom row)
            lowest_yellow = max(yellow_rows)

            # Fill all pixels above the lowest yellow pixel with yellow (up to row 0)
            for row in range(0, lowest_yellow + 1):
                output_grid[row, col] = 4

    return output_grid.tolist()