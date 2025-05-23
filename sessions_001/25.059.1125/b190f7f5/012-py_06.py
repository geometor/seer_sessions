"""
The transformation rule can be described as follows:

1. **Dynamic Output Grid:** The output grid's dimensions are determined by multiplying the input grid's dimensions by 3. Create an output grid filled with white (0) pixels.
2. **Azure Removal:** Ignore azure (8) pixels in the input grid; they don't affect the output.
3. **Colored Pixel Replication:** For each yellow (4), blue (1), and red (2) pixel in the input grid:
    - Calculate the top-left corner coordinates in the output grid by multiplying the input row and column indices by 3.
    - Create a "plus" shape centered at the calculated coordinates with the color of the input pixel. The plus extends one pixel in each cardinal direction (up, down, left, right) from the center.  The plus is truncated if it would extend beyond the output grid boundaries.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid based on input_grid size, multiplied by 3
    output_rows = input_grid.shape[0] * 3
    output_cols = input_grid.shape[1] * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through the input grid
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            color = input_grid[r, c]

            # skip azure (8) and white (0)
            if color == 8 or color == 0:
                continue

            # calculate the center coordinates for the plus shape
            out_r = r * 3
            out_c = c * 3

            # Create the plus shape, ensuring it stays within bounds
            if out_r > 0:
                output_grid[out_r - 1, out_c] = color  # Up
            if out_r < output_rows - 1:
                output_grid[out_r + 1, out_c] = color  # Down
            if out_c > 0:
                output_grid[out_r, out_c - 1] = color  # Left
            if out_c < output_cols - 1:
                output_grid[out_r, out_c + 1] = color  # Right
            output_grid[out_r, out_c] = color  # Center

    return output_grid