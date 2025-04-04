"""
1.  **Identify Objects:** Locate the 2x2 blue square (color 1) and the 2x2 red square (color 2) within the input grid.

2.  **Process Blue Square:**
    *   Disassemble the 2x2 blue square into four individual blue pixels.
    *   Place the first blue pixel in the first column (column 0) of the same row where the blue square started.
    *   Place the remaining three blue pixels diagonally, one pixel down and one pixel to the right for each subsequent pixel.

3.  **Process Red Square:**
    *    Move the red square to the last two columns of the grid, aligned to the same starting row.
    *   Find the row of the input grid that corresponds to a y-offset of +3 from the original red square location and put a red pixel in the last column. Do the same for +4.
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
    # Initialize output_grid as a zero-filled array of the same size/shape as input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

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
        output_grid[red_row, cols-2:cols] = 2
        output_grid[red_row + 1, cols-2:cols] = 2
        # additional red pixels based on the original red square location
        output_grid[red_row + 3, cols -1] = 2
        output_grid[red_row + 4, cols -1] = 2


    return output_grid