"""
The transformation rule preserves the original blue (1), red (2), and magenta (6) pixels in their original positions. 
It then adds yellow (4) pixels in relation to the red (2) pixels and orange (7) pixels in relation to the blue (1) pixels.

For each red pixel (2):
    - Place a yellow pixel (4) one row above it.
    - Place another yellow pixel (4) two positions to the left of the first yellow one.
    - Place another yellow pixel (4) two positions to the right of the first yellow one.

For each blue pixel (1):
  - Add orange pixels (7) cardinally adjacent below, left and right.
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
                # Add yellow pixels above, two to the left and two to the right
                if r - 1 >= 0:
                    output_grid[r - 1, c] = 4
                    if c - 2 >= 0 :
                        output_grid[r-1,c-2] = 4
                    if c+2 < cols:
                        output_grid[r-1, c+2] = 4
            elif input_grid[r, c] == 1:  # Blue pixel
                # Add orange pixels below, left, and right
                if r + 1 < rows:
                    output_grid[r + 1, c] = 7
                if c - 1 >= 0:
                    output_grid[r, c - 1] = 7
                if c + 1 < cols:
                    output_grid[r, c + 1] = 7

    return output_grid