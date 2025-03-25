"""
The output grid always has 3 columns: the leftmost, center, and rightmost columns of the input grid.
The rows included in the output grid are determined by the rows where there is a non-zero pixel in the
leftmost, center, or rightmost columns of the input grid. Only these selected rows are kept, in their
original order, to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by selecting specific columns and rows based on non-zero values.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    input_np = np.array(input_grid)
    num_cols = input_np.shape[1]

    # 1. Identify Key Columns
    left_col_idx = 0
    right_col_idx = num_cols - 1
    center_col_idx = num_cols // 2

    # Handle edge cases where there might be fewer than 3 columns
    if num_cols == 1:
      column_indices = [left_col_idx]
    elif num_cols == 2:
      column_indices = [left_col_idx, right_col_idx]
    else:
      column_indices = [left_col_idx, center_col_idx, right_col_idx]


    # 2. Identify Key Rows
    key_rows = set()
    for row_idx in range(input_np.shape[0]):
        for col_idx in column_indices:
            if input_np[row_idx, col_idx] != 0:
                key_rows.add(row_idx)
                break  # Move to the next row once a non-zero is found

    # 3. Construct Output Grid
    # First, select the key columns
    temp_grid = input_np[:, column_indices]

    # Then, select only the key rows from the temporary grid, preserving order
    sorted_key_rows = sorted(list(key_rows))
    output_grid = temp_grid[sorted_key_rows]

    return output_grid.tolist()