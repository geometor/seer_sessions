"""
Transforms a 3x3 input grid into a 5x5 output grid by selectively duplicating rows and columns.

Rows at indices 0 and 2 are duplicated vertically. The row at index 1 is kept as is.
Columns at indices 0 and 2 are duplicated horizontally. The column at index 1 is kept as is.

This results in:
- Corner cells (0,0), (0,2), (2,0), (2,2) becoming 2x2 blocks.
- Edge cells (0,1), (2,1) becoming 2x1 blocks.
- Edge cells (1,0), (1,2) becoming 1x2 blocks.
- Center cell (1,1) becoming a 1x1 block.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row and column duplication transformation.

    Args:
        input_grid (np.ndarray): A 3x3 NumPy array representing the input grid.

    Returns:
        np.ndarray: A 5x5 NumPy array representing the transformed output grid.
    """
    input_np = np.array(input_grid)
    input_height, input_width = input_np.shape

    # Determine middle row and column indices (assuming odd dimensions like 3x3)
    middle_row = input_height // 2
    middle_col = input_width // 2

    # 1. Perform row duplication
    intermediate_rows = []
    for r in range(input_height):
        intermediate_rows.append(input_np[r])
        # Duplicate row if it's not the middle row
        if r != middle_row:
            intermediate_rows.append(input_np[r])
    
    intermediate_grid = np.array(intermediate_rows)
    
    # 2. Perform column duplication
    output_cols = []
    for c in range(input_width):
        output_cols.append(intermediate_grid[:, c])
        # Duplicate column if it's not the middle column
        if c != middle_col:
             output_cols.append(intermediate_grid[:, c])

    # Combine the columns to form the final output grid
    # Note: np.array(output_cols) creates rows from columns, so transpose is needed.
    output_grid = np.array(output_cols).T 

    return output_grid
