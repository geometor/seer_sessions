"""
The transformation replicates a two-row pattern: an "original" row and a "duplicated" row, throughout the entire grid.

1.  **Initialization:** Create an output grid of the same dimensions as the input grid, filled with zeros.
2.  **Iterate through Rows:** Process the grid in pairs of rows: an "original" row and a "duplicated" row.
3.  **Original Row:** For the original row (even index in the output grid, starting at 0), copy the entire row from the input grid at the index `y // 2` to the output grid at index `y`.
4.  **Duplicated Row:** For the duplicated row (odd index in the output grid, starting at 1):
    *   Iterate through each pixel in the corresponding "original" row (index `y // 2` in the input grid).
    *   If a pixel in the original row is non-zero:
        *   Let `x` be the column index of the non-zero pixel in the original row.
        *   Let `color` be the value (color) of that pixel.
        *   Place the `color` at positions `2 * x` and `2 * x + 1` in the current (duplicated) row of the output grid. Make sure you do not exceed the bounds of output grid width.
5.  **Repeat:** Continue this process for all pairs of rows until the entire output grid is filled.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Iterate through each row of the *output* grid
    for y in range(height):
        # Original Row: Copy from input to output (even rows)
        if y % 2 == 0:
            output_grid[y] = input_grid[y // 2]
        # Duplicated Row: Process based on corresponding original row in input (odd rows)
        else:
            original_row_index = y // 2
            for x in range(width):
                color = input_grid[original_row_index, x]
                if color != 0:
                    # Duplicate the color at positions 2*x and 2*x+1
                    new_x_1 = 2 * x
                    new_x_2 = 2 * x + 1

                    # Ensure we don't go out of bounds
                    if new_x_1 < width:
                        output_grid[y, new_x_1] = color
                    if new_x_2 < width:
                        output_grid[y, new_x_2] = color

    return output_grid