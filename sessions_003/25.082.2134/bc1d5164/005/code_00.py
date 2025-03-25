"""
Extracts a subgrid based on column and row criteria. The output grid always includes the leftmost, center, and rightmost columns
of the input grid (or fewer if the input grid has fewer than 3 columns). A row is included in the output grid if and only if,
for each of the selected key columns, all non-zero pixels within that row in the corresponding column of the input grid have
the same color/value.
"""

import numpy as np

def _get_key_columns(input_grid):
    """Helper function to get the key column indices."""
    num_cols = len(input_grid[0])
    if num_cols == 1:
        return [0]
    elif num_cols == 2:
        return [0, 1]
    else:
        return [0, num_cols // 2, num_cols - 1]

def _check_row(input_grid, row_index, key_columns):
    """Helper function to check if a row should be selected."""
    for col_index in key_columns:
        # Extract non-zero pixels in the current key column for the given row
        values = []
        for r_idx in range(len(input_grid)):
             if r_idx == row_index:
                if input_grid[r_idx][col_index] != 0:
                    values.append(input_grid[r_idx][col_index])

        # Check if all non-zero values are the same
        if len(values) > 0:
            if not all(v == values[0] for v in values):
              return False
    return True
    

def transform(input_grid):
    """
    Transforms the input grid by selecting specific columns and rows based on criteria.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the output grid.
    """
    input_np = np.array(input_grid)

    # 1. Identify Key Columns
    key_columns = _get_key_columns(input_grid)

    # 2. Select Key Columns Subgrid
    intermediate_grid = input_np[:, key_columns].tolist()

    # 3. Select Rows
    selected_rows = []
    for row_idx in range(len(input_grid)):
        if _check_row(input_grid, row_idx, key_columns):
            selected_rows.append(row_idx)
            
    # 4. Construct Output Grid
    output_grid = []
    for row_idx in selected_rows:
            output_grid.append(intermediate_grid[row_idx]) #access via index because it could be empty


    return output_grid