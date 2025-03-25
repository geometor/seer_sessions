"""
1.  **Input:** A grid of any size containing pixels of various colors, including maroon (9).

2.  **Output:** A 3x3 grid.

3.  **Transformation Rule:**
    *   Examine the input grid and locate all maroon pixels within the top-left 3x3 area of the input grid.
    *   The output grid will always be 3x3.
    *   Consider only the first three rows and first three columns of the input.
    *   Within the top-left 3x3 area, map the columns to rows and rows to columns - reflecting across the diagonal.
        If the *input* coordinate is (r, c), the *output* coordinate is (c, r).
    *   If a pixel within the considered input area is maroon (9), place a red (2) pixel in output grid in the transformed coordinate (c, r).
    *   Fill all other cells of the output grid with white (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 3x3 filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Consider only the top-left 3x3 region of the input
    for r in range(min(3, input_grid.shape[0])):
        for c in range(min(3, input_grid.shape[1])):
            # Check if the pixel is maroon (9)
            if input_grid[r, c] == 9:
                # Reflect across the diagonal: (r, c) -> (c, r)
                output_grid[c, r] = 2  # Set corresponding output pixel to red (2)

    return output_grid