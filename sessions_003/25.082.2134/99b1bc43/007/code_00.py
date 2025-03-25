"""
1. Identify Subgrid A: Determine the portion of the input grid *above* the first row that consists entirely of yellow (4) pixels. This is Subgrid A.
2. Create Output Grid: Initialize a 4x4 output grid filled with black (0) pixels.
3. Get Subgrid A dimenstions: Get the height and width of Subgrid A.
4. Map Blue Pixels: Iterate through Subgrid A. For each blue pixel (value 1) encountered at row `r` and column `c`:
    *   Calculate the corresponding output row as `height of Subgrid A - 1 - r`
    *   Calculate the corresponding output column as `width of Subgrid A - 1 - c`.
    *   Set the pixel at the calculated output row and column in the output grid to green (3).
5. Return Output: Return the 4x4 output grid.
"""

import numpy as np

def transform(input_grid):
    # Identify Subgrid A.
    input_grid = np.array(input_grid)
    yellow_row_index = np.where((input_grid == 4).all(axis=1))[0][0]
    subgrid_a = input_grid[:yellow_row_index]

    # Create Output Grid.
    output_grid = np.zeros((4, 4), dtype=int)

    # Get Subgrid A dimensions
    height_a = subgrid_a.shape[0]
    width_a = subgrid_a.shape[1]

    # Map Blue Pixels.
    for r_a, row in enumerate(subgrid_a):
        for c_a, pixel in enumerate(row):
            if pixel == 1:
                r_o = height_a - 1 - r_a  # output row
                c_o = width_a - 1 - c_a  # output col
                output_grid[r_o, c_o] = 3

    return output_grid