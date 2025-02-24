"""
1.  **Initialization:** Create an output grid that's larger than the input grid. Specifically, add one row above and below the input grid dimensions and increase the width by two.
2.  **Padding border:** Add a border of '0' (white) pixels around the expanded region where the input will be placed. The padding should be one pixel.
3.  **Copy and Expand:** Copy each element from the input grid to the output grid. Expand as follows:
    *   Copy the top row of the input into the output, bordered by white pixels
    *   duplicate the top row of the input and add under the top row, mirroring each pixel
    *   Copy the bottom row of the input grid to output grid, under the duplicated input top row.
    *  duplicate the bottom row of the input and add under it, mirroring each pixel, padding left and right with white.
"""

import numpy as np

def transform(input_grid):
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows + 2
    output_cols = input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy the top row of the input, and pad
    output_grid[0, 1:output_cols-1] = input_grid[0]

    # duplicate the top row of the input and add under the top row, mirroring each pixel
    output_grid[1, 1:output_cols-1] = input_grid[0]

    # Copy the bottom row of the input grid to output grid, under the duplicated input top row.
    output_grid[2, 1:output_cols-1] = input_grid[1]

    # duplicate the bottom row of the input and add under it, mirroring each pixel, padding left and right with white.
    output_grid[3, 1:output_cols-1] = input_grid[1]

    return output_grid