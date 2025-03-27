"""
Analyzes the input grid and performs transformations based on the presence of zero-filled rows or columns.

If zero-filled columns are present, the grid is duplicated vertically, and a row of zeros is inserted.
If zero-filled rows are present, a column of zeros is inserted in the middle of the grid.
"""

import numpy as np

def analyze_grid(grid):
    np_grid = np.array(grid)
    rows, cols = np_grid.shape
    zero_rows = [i for i, row in enumerate(np_grid) if np.all(row == 0)]
    zero_cols = [j for j in range(cols) if np.all(np_grid[:, j] == 0)]
    return rows, cols, zero_rows, zero_cols

def transform(input_grid):
    # Analyze the input grid
    input_np = np.array(input_grid)
    input_rows, input_cols, input_zero_rows, input_zero_cols = analyze_grid(input_np)

    # Case 1: Zero-filled columns (Example 1 Pattern)
    if input_zero_cols:
        # Duplicate the grid vertically
        duplicated_grid = np.vstack([input_np, input_np])
        # Create a zero row
        zero_row = np.zeros((1, input_cols), dtype=int)
        # Insert the zero row after the original input
        output_grid = np.insert(duplicated_grid, input_rows, zero_row, axis=0)

    # Case 2: Zero-filled rows (Example 2 Pattern)
    elif input_zero_rows:
        # Create a zero column
        zero_col = np.zeros((input_rows, 1), dtype=int)
        # Insert the zero column in the middle
        output_grid = np.insert(input_np, input_cols, zero_col, axis=1)
    else: # Default - No change.  We don't have information on how to proceed
          # so just return the input as a fallback.
        output_grid = input_np

    return output_grid.tolist()