"""
1.  **Resize:** The output grid has the same number of rows as the input grid, but its width is half the width of the input grid (using integer division).

2.  **Color Transformation:** Iterate through each cell of the *output* grid, considering the corresponding cell in the *input* grid (same row, same column index).
    *   If the input cell is green (3) or yellow (4), the output cell becomes magenta (6).
    *   If the input cell is white (0), and there's *any* green (3) or yellow(4) to its *right* on the *same row* in the *input grid*, then the output cell becomes magenta (6).
    *    Otherwise the output cell takes the input cells value.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid. Resize to half the width of the input.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    output_cols = cols // 2
    output_grid = output_grid[:, :output_cols]


    # Iterate through the *output* grid's dimensions.
    for i in range(rows):
        for j in range(output_cols):
            # Get the corresponding input pixel.
            input_pixel = input_grid[i, j]

            # Apply color transformation rules.
            if input_pixel == 3 or input_pixel == 4:
                output_grid[i, j] = 6
            elif input_pixel == 0:
                # Check for 3 or 4 to the right in the input grid.
                if np.any((input_grid[i, j+1:] == 3) | (input_grid[i, j+1:] == 4)):
                    output_grid[i, j] = 6
                #else keep original value, already done by array copy

    return output_grid