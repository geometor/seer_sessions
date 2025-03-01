"""
1.  **Locate Blue Regions:** Identify all blue (1) pixels in the input grid.  These pixels may form a continuous vertical line or a broken vertical line.
2.  **Recolor Blue:** Change the color of all identified blue (1) pixels to red (2).
3.  **Expand Canvas:** Add three rows to the bottom of the grid.
4.  **Extend Red Vertically:** For each column that contained a blue (now red) pixel in the original grid, extend the red color vertically downwards into the three newly added rows.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with increased height
    input_height, input_width = input_grid.shape
    output_height = input_height + 3
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Copy original grid, recoloring blue to red
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 1:
                output_grid[row, col] = 2
            else:
                output_grid[row, col] = input_grid[row, col]

    # Find columns with blue pixels (now red in output_grid)
    cols_with_blue = np.unique(np.argwhere(output_grid[:input_height, :] == 2)[:, 1])

    # Extend red vertically into added rows
    for row in range(input_height, output_height):
        for col in cols_with_blue:
            output_grid[row, col] = 2

    return output_grid