"""
1.  **Identify Red Pixels:** Locate all pixels with the value '2' (red) in the input grid.

2.  **Conditional Blue Transformation:** For *each* red pixel, determine if it should be changed to blue ('1') based on the following rule:
    * A red pixel is changed to blue if it is *either*:
        * The last (bottom-most) red pixel in its column.
        * The last (right-most) red pixel in its row *given the input*.

3. Copy all other pixels to output without change.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all red pixel coordinates
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))

    # Apply the transformation rules
    for r, c in red_pixels:
        # Check if it's the last red in its column
        last_red_in_col = True
        for r2 in range(r + 1, rows):
            if input_grid[r2, c] == 2:
                last_red_in_col = False
                break

        # Check if it's the last red in its row
        last_red_in_row = True
        for c2 in range(c + 1, cols):
            if input_grid[r, c2] == 2:
                last_red_in_row = False
                break

        # Change to blue if either condition is met
        if last_red_in_col or last_red_in_row:
            output_grid[r, c] = 1

    return output_grid