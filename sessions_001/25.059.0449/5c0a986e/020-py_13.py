"""
1.  **Create Output Grid:** Create a new output grid. The number of rows will be the same as the number of rows in the input. The number of columns will be the number of columns of the input plus 2.

2.  **Process Blue Square:**
    *   Locate the 2x2 blue square in the input grid.
    *   Disassemble the 2x2 blue square into four individual blue pixels.
    *   Place the first blue pixel in the first column (column 0) of the row where the blue square was found.
    *   Place the remaining three blue pixels diagonally, one pixel down and one pixel to the right for each subsequent pixel.

3.  **Process Red Square:**
    *   Locate the 2x2 red square in the input grid.
    *   Place an identical 2x2 red square in the last two columns of the output, starting from the same row where the red square was found in the input.
    *   Starting from an offset of +3 rows from the original red square row, fill the last column of the output grid with red, until the last row.
"""

import numpy as np

def find_square(grid, color, size=2):
    """Finds a square of a given color and size."""
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                return r, c
    return None, None

def transform(input_grid):
    # Initialize output_grid with updated dimensions
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols + 2), dtype=int)

    # Find the blue square.
    blue_row, _ = find_square(input_grid, 1)
    if blue_row is not None:
        # Place blue pixels diagonally.
        for i in range(4):
            output_grid[blue_row + i, i] = 1

    # Find the red square.
    red_row, red_col = find_square(input_grid, 2)
    if red_row is not None:
        # Place red square in the last two columns.
        output_grid[red_row, cols:cols+2] = 2
        output_grid[red_row + 1, cols:cols+2] = 2

        # Additional red pixels based on the original red square location.
        for i in range(red_row + 3, rows):
            output_grid[i, cols + 1] = 2

    return output_grid