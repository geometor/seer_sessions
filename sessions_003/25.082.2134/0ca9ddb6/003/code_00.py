"""
1.  **Preservation:** The original blue (1), red (2), magenta (6) and azure (8) pixels remain in their original positions in the output grid.

2.  **Yellow Pixel Placement:** For each red pixel (2) in the input grid:
    *   Place a yellow pixel (4) one row *below* it.
    *   Place another yellow pixel (4) two positions to the *left* of the first yellow one (one row below and 2 columns left of original red).
    *   Place another yellow pixel (4) two positions to the *right* of the first yellow one (one row below and 2 columns right of original red).

3.  **Orange Pixel Placement:** For each blue pixel (1) in the input grid:
    *   Place an orange pixel (7) directly below it.
    *   Place an orange pixel (7) directly to the left of it.
    *   Place an orange pixel (7) directly to the right of it.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find red and blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Red pixel
                # Add yellow pixels below, two to the left and two to the right
                if r + 1 < rows:
                    output_grid[r + 1, c] = 4
                    if c - 2 >= 0 :
                        output_grid[r+1,c-2] = 4
                    if c+2 < cols:
                        output_grid[r+1, c+2] = 4
            elif input_grid[r, c] == 1:  # Blue pixel
                # Add orange pixels below, left, and right
                if r + 1 < rows:
                    output_grid[r + 1, c] = 7
                if c - 1 >= 0:
                    output_grid[r, c - 1] = 7
                if c + 1 < cols:
                    output_grid[r, c + 1] = 7

    return output_grid