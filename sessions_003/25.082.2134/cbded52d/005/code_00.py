"""
The transformation identifies the first non-zero row in the input grid. Then, it identifies "target rows" which are every other non-zero row, starting with the first. For each target row, the values in the 2nd and 5th columns are replaced with the values from the corresponding columns of the first non-zero row. The rest of the grid remains unchanged.
"""

import numpy as np

def _find_first_non_zero_row(grid):
    """Helper function to find the index of the first non-zero row."""
    for i, row in enumerate(grid):
        if np.any(row != 0):
            return i
    return -1  # Return -1 if no non-zero row is found

def _find_target_rows(grid, first_non_zero_row):
    """Helper function to find the indices of the target rows."""
    target_rows = []
    non_zero_count = 0
    for i, row in enumerate(grid):
        if np.any(row != 0):
            non_zero_count += 1
            if non_zero_count % 2 != 0:
                target_rows.append(i)
    return target_rows

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find the First Non-Zero Row
    first_non_zero_row = _find_first_non_zero_row(input_grid)

    if first_non_zero_row == -1:
        return output_grid.tolist() #return the unchanged grid since there will be no target rows

    # 2. Identify Target Rows
    target_rows = _find_target_rows(input_grid, first_non_zero_row)

    # 3. Replace Values in Target Columns
    for row_index in target_rows:
        if cols > 1:
            output_grid[row_index, 1] = input_grid[first_non_zero_row, 1]
        if cols > 4:
            output_grid[row_index, 4] = input_grid[first_non_zero_row, 4]
    
    # 4. The modified grid is the output.
    return output_grid.tolist()