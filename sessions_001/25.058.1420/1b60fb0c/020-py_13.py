"""
1.  Row-wise Processing: The transformation occurs independently for each row of the input grid.
2.  Horizontal Scan: Within each row, scan from left to right.
3.  Blue Pixel Anchor: Identify the left-most blue pixel (if any) in the current row.
4.  White to Red Conversion: All white pixels to the *left* of this blue pixel's column should be changed to red. If no blue is in the row, do not change white to red.
5.  Preservation: Blue pixels, and any other pixels that are *not* white and to the left of a blue, are preserved with their original color.
"""

import numpy as np

def find_leftmost_blue(row):
    """Finds the column index of the leftmost blue pixel in a row."""
    for col, pixel in enumerate(row):
        if pixel == 1:  # Blue pixel
            return col
    return -1  # No blue pixel found

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)  # Start with a copy
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find the leftmost blue pixel's column in the current row
        blue_col = find_leftmost_blue(input_grid[r])

        # If a blue pixel was found, change white pixels to the left
        if blue_col != -1:
            for c in range(blue_col):
                if output_grid[r, c] == 0:  # White pixel
                    output_grid[r, c] = 2  # Change to red

    return output_grid