"""
1. Examine Input: Determine the dimensions of the input grid and check for the presence of all-zero rows.
2. Conditional Stacking and Zero Insertion:
    *   If the input grid contains any all-zero rows: Duplicate the input grid horizontally. Insert a column of zeros between the two copies of the input.
    *   If the input grid does NOT contain any all-zero rows: Duplicate the input grid vertically. Stack two copies of the input. Add one row of zeros between the two copies of the input.
"""

import numpy as np

def find_zero_rows(grid):
    # Convert to numpy array for easier processing
    grid_np = np.array(grid)
    zero_rows = []
    for i, row in enumerate(grid_np):
        if np.all(row == 0):
            zero_rows.append(i)
    return zero_rows

def transform(input_grid):
    # Convert input grid to numpy array
    input_np = np.array(input_grid)
    rows, cols = input_np.shape

    # Check for existing zero rows
    zero_rows = find_zero_rows(input_np)

    if zero_rows:  # Example 2 style: existing zero row(s)
        # Duplicate the input grid horizontally
        duplicated_grid = np.hstack([input_np, input_np])

        # Create a zero column
        zero_col = np.zeros((rows, 1), dtype=int)

        # Insert the zero column
        output_grid = np.insert(duplicated_grid, cols, zero_col, axis=1)

    else: # Example 1 style: no zero rows
        # Duplicate the input grid vertically
        duplicated_grid = np.vstack([input_np, input_np])

        # Create a zero row
        zero_row = np.zeros((1, cols), dtype=int)

        # Insert the zero row between the two input grids
        output_grid = np.insert(duplicated_grid, rows, zero_row, axis=0)

    return output_grid.tolist()