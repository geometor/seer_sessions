"""
1.  **Identify Blue Pixels:** Scan the input grid and find all pixels with a value of 1 (blue).
2.  **Check to the Right:** For each blue pixel, check if to the right of the position exist and if the exist and it contains 0, change the color from 0 to 2.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Identify Blue Pixels
            if input_grid[r, c] == 1:
                # Check to the Right and change from 0 to 2.
                if c + 1 < cols and output_grid[r, c+1] == 0:
                  output_grid[r,c+1] = 2
    return output_grid