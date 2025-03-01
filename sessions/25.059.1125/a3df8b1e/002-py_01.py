"""
The transformation rule is as follows:

1. Observe the input grid. Note its height, width, and the column index of the single blue (1) pixel in the bottom row.
2. Create an output grid with the same height and width as the input grid.
3. Iterate through each cell of the output grid, row by row, column by column.
4. Start filling columns with the blue pixel, shifting its location up by one row in each subsequent column, until it is in the first row, at which point the location resets back to the bottom row and repeats this behaviour.
5. The row that contains the blue pixel shifts by one column to the right from its position in the previous column.
6. Fill all the remaining cells with white pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the column index of the blue pixel in the input grid
    blue_col = np.where(input_grid[-1] == 1)[0][0]

    # Generate the output pattern
    for j in range(cols):
        blue_row = rows - 1 - ((j + blue_col) % rows)  # Calculate the row index for the blue pixel
        output_grid[blue_row, j] = 1

    return output_grid