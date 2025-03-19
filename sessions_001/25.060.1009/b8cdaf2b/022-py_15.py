"""
1.  **Identify the third row:** Locate the third row from the top of the input grid (index 2).
2.  **Modify the third row:** Change the color of the leftmost pixel (index 0) and the rightmost pixel (index -1) of the third row to blue (color code 1).
3.  **Preserve other pixels:** All other pixels in the input grid remain unchanged and are copied to the output grid. If a third row doesn't exist, the output is the same as the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]

    # Check if there are at least 3 rows before proceeding
    if rows >= 3:
        # Change the color of the leftmost and rightmost pixels of the third row to blue (1)
        output_grid[2, 0] = 1
        output_grid[2, -1] = 1

    return output_grid