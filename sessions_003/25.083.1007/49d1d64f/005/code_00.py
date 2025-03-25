"""
The program takes each input pixel and turns it into a 2x2 block of the same color. Then, it adds a border of '0' (white) color.  The border is added such that the final dimensions are increased by one row at the top and one at the bottom, and one column on the left and one column on the right.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Rows
    duplicated_rows_grid = []
    for row in input_grid:
        duplicated_rows_grid.append(row)
        duplicated_rows_grid.append(row)
    
    # Duplicate Columns
    duplicated_cols_grid = []
    for row in duplicated_rows_grid:
        new_row = []
        for cell in row:
            new_row.append(cell)
            new_row.append(cell)
        duplicated_cols_grid.append(new_row)

    # Convert to numpy array for easier manipulation
    expanded_grid = np.array(duplicated_cols_grid)

    # Add 0 border - correct dimensions
    rows, cols = expanded_grid.shape
    output_grid = np.zeros((rows + 2, cols + 2), dtype=int)
    output_grid[1:rows+1, 1:cols+1] = expanded_grid  # Place expanded grid inside the border

    return output_grid.tolist()