"""
The task involves identifying a specific row or column based on a color pattern within the input grid (either entirely white or predominantly a single non-white color) and replacing all values in that row/column with the color red.
"""

import numpy as np

def find_target_row(grid):
    """Finds the first row that is entirely white (value 0)."""
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 0):
            return r
    return None

def find_target_column(grid, dominant_color):
    """
    Finds the first column that is predominantly of the 'dominant_color'
    (allowing for interspersed white pixels).
    """
    rows, cols = grid.shape
    for c in range(cols):
        column_values = grid[:, c]
        #count dominant excluding white
        non_white_count = np.sum(column_values != 0)
        dominant_count = np.sum(column_values == dominant_color)

        if non_white_count > 0 and dominant_count / non_white_count >= 0.8:
            return c
    return None

def transform(input_grid):
    """
    Transforms the input grid by inserting a red line. The line is placed
    in the first all-white row, or if no all-white row exists, it is placed
    in the first mostly a single non-white color column.  All cells of line are
    converted to red.
    """
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find target row (all white)
    target_row = find_target_row(output_grid)

    if target_row is not None:
        # Insert horizontal red line
        output_grid[target_row, :] = 2
    else:
        # Find target column (predominantly non-white)
        # Determine dominant non-white color (excluding 0, which is white)
        unique, counts = np.unique(input_grid[input_grid != 0], return_counts=True)

        if len(unique) > 0:
            dominant_color = unique[np.argmax(counts)]
            target_col = find_target_column(output_grid, dominant_color)

            if target_col is not None:
                #insert vertical red line
                output_grid[:, target_col] = 2

    return output_grid