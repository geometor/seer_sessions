"""
If a column contains a yellow pixel and that column is next to the all-white column on the left, prepend magenta pixels to the whole yellow-containing column.
"""

import numpy as np

def is_column_all_white(grid, col_index):
    """Checks if a specified column in the grid is entirely white (color 0)."""
    rows = grid.shape[0]
    for i in range(rows):
        if grid[i, col_index] != 0:
            return False
    return True

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # Initialize output_grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = output_grid.tolist()

    # Iterate through columns, starting from the second column (index 1).
    for j in range(1, cols):
        # Check if the left neighbor column is all white.
        if is_column_all_white(input_grid, j - 1):
            # Check if the current column contains any yellow pixels.
            has_yellow = False
            for i in range(rows):
                if input_grid[i][j] == 4:
                    has_yellow = True
                    break

            # If the left neighbor is all white and the current column has yellow,
            # prepend 6 to every cell in the current column.
            if has_yellow:
                for i in range(rows):
                    output_grid[i].insert(j, 6)

    return np.array(output_grid)