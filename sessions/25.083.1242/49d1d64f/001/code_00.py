"""
The input grid's rows and columns are duplicated, and then a border of '0' (white) pixels is added around the expanded grid.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Rows
    duplicated_rows_grid = []
    for row in input_grid:
        duplicated_rows_grid.append(row)
        duplicated_rows_grid.append(row)  # Add the row again to duplicate

    duplicated_rows_grid = np.array(duplicated_rows_grid)

    # Duplicate Columns
    duplicated_cols_grid = []
    for row in duplicated_rows_grid:
        new_row = []
        for cell in row:
            new_row.append(cell)
            new_row.append(cell) #add the cell again
        duplicated_cols_grid.append(new_row)

    duplicated_cols_grid = np.array(duplicated_cols_grid)

    # Add Border
    height, width = duplicated_cols_grid.shape
    output_grid = np.zeros((height + 2, width + 2), dtype=int)  # Initialize with zeros
    output_grid[1:height+1, 1:width+1] = duplicated_cols_grid #copy the inside

    return output_grid