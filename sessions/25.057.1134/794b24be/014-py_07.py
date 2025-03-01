"""
1.  **Identify Blue Pixels:** Locate all pixels in the `input_grid` with a value of '1' (blue).

2.  **Mirror Blue Pixels across Y Axis** For each identified blue pixel:
    *   If it is in column index `c`, map it to `3 - 1 - c` in output

3.  **Change to Red:**  Set color of mapped pixel to `2` (red).

4.  **All unmapped positions are set to zero**

5.  **Everything Else:** All other pixels in the `output_grid` remain '0' (white).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # Initialize the output grid as a copy of the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid to find blue pixels.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                # Mirror blue pixels across the Y axis
                new_c = cols - 1 - c
                # Change blue pixels to red in the output grid.
                output_grid[r, new_c] = 2

    return output_grid