"""
1.  **Identify Yellow Regions:** Locate all contiguous blocks (or individual pixels) of color `4` (yellow) within the input grid.
2.  **Downward Expansion:** For each yellow region, extend it downwards.  This means changing all `0` (white) pixels directly below any yellow pixel to `4` (yellow).
3.  **Boundary Condition:** Continue the downward expansion until the bottom edge of the grid is reached.  The overall size of the grid remains constant. Essentially, yellow 'falls' or 'fills down' the grid.
4. **Preserve Grid Size.** Make sure there are no new rows and the number of rows in the output equals the number of rows in the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each column
    for j in range(cols):
        # Find the topmost yellow pixel in the column
        yellow_found = False
        for i in range(rows):
            if input_grid[i][j] == 4:
                yellow_found = True
            # If a yellow pixel has been found, fill downwards
            if yellow_found:
                output_grid[i][j] = 4

    return output_grid