"""
1. **Expand Grid:** Double the dimensions of the input grid to create the output grid.
2. **Magenta Placement (Top-Left Rule):** For each magenta pixel (value '6') in the input grid, place a magenta pixel in the top-left corner of the corresponding 2x2 block in the output grid. Specifically, if a magenta pixel is at `(r, c)` in the input, place a magenta pixel at `(2r, 2c)` in the output.
3. **Azure Border:** If an input grid row contains one or more '6' pixels, draw a solid line of '8' pixels across the *entire* corresponding *expanded* output rows. For each row `r` in input, rows `2r` and `2r+1` in output, should have '8' values if row `r` contains a 6.
4.  **Fill Remaining:** Fill all remaining empty cells (not occupied by '6' or '8') in the output grid with black pixels ('0').
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Magenta Placement (Top-Left Rule)
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] == 6:
                output_grid[2 * r, 2 * c] = 6

    # Azure Border
    for r in range(input_height):
        if 6 in input_grid[r]:  # Check if the row contains a 6
            output_grid[2 * r, :] = 8
            output_grid[2 * r + 1, :] = 8

    # Fill Remaining with 0, overwriting any incorrect assignments
    for r in range(output_height):
        for c in range(output_width):
            if output_grid[r,c] == 0:
                continue
            if output_grid[r,c] !=6 and output_grid[r,c] !=8:
                 output_grid[r, c] = 0

    return output_grid