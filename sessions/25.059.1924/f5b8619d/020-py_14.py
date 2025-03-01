"""
1.  **Double the Grid:** Create an output grid that is twice the size of the input grid in both dimensions (rows and columns).

2.  **Process Each Input Pixel:** For each pixel in the input grid, at row `r` and column `c`, perform the following based on the pixel's color:

    *   **White (0):** Create a 2x2 block of white pixels in the output grid. The top-left corner of this block is at position (2*r, 2*c).
        *   output_grid[2*r, 2*c] = 0
        *   output_grid[2*r + 1, 2*c] = 0
        *   output_grid[2*r, 2*c + 1] = 0
        *   output_grid[2*r + 1, 2*c + 1] = 0

    *   **Yellow (4):** Create a 2x2 block in the output grid, with a yellow pixel in the top-left corner and azure pixels in the other three positions. The top-left corner of this block is at position (2*r, 2*c).
        *   output_grid[2*r, 2*c] = 4
        *   output_grid[2*r + 1, 2*c] = 8
        *   output_grid[2*r, 2*c + 1] = 8
        *   output_grid[2*r + 1, 2*c + 1] = 8
3. **No other colors exist.** The examples only contain white and yellow colors.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = 2 * input_rows, 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    for r in range(input_rows):
        for c in range(input_cols):
            # Replicate white pixels
            if input_grid[r, c] == 0:
                output_grid[2*r, 2*c] = 0
                output_grid[2*r+1, 2*c] = 0
                output_grid[2*r, 2*c+1] = 0
                output_grid[2*r+1, 2*c+1] = 0
            # Transform and replicate yellow pixels
            elif input_grid[r, c] == 4:
                output_grid[2*r, 2*c] = 4
                output_grid[2*r+1, 2*c] = 8
                output_grid[2*r, 2*c+1] = 8
                output_grid[2*r+1, 2*c+1] = 8

    return output_grid