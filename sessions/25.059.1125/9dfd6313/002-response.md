# 9dfd6313 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify '5' Anchors:** Find all columns in the input grid that contain the value '5'.  These columns, and their original order, will remain fixed in the output.

2.  **Process Non-'5' Columns:** For each of the remaining columns in *input*, scanning from left to right, gather all non-zero values into a list, maintaining their original top-to-bottom order.

3.  **Place Non-'5' Values:** Beginning with the first column *after* the last '5' column in the *output*, begin filling in the non-zero lists created in step 2. Each list of non-zero values is placed top-to-bottom in the first available column of the *output*.

4. **Fill Remaining Cells:** The remaining cells, if any, of the output grid are then filled by `0`.
"""

import numpy as np

def get_columns_with_value(grid, value):
    """
    Returns a list of column indices that contain at least one cell with the given value.
    """
    cols_with_value = []
    for j in range(grid.shape[1]):
        if value in grid[:, j]:
            cols_with_value.append(j)
    return cols_with_value

def get_nonzero_values_from_columns(grid, cols):
    """
    Extracts all non-zero values from the specified columns, maintaining order.
    Returns a list of lists, where each inner list represents a column.
    """
    nonzero_values = []
    for j in cols:
      col_values = []
      for i in range(grid.shape[0]):
          if grid[i,j] != 0:
            col_values.append(grid[i,j])
      nonzero_values.append(col_values)
    return nonzero_values
  
def transform(input_grid):
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Identify '5' Anchors
    five_cols = get_columns_with_value(input_grid, 5)
    for col_index in five_cols:
        output_grid[:, col_index] = input_grid[:, col_index]

    # 2. Process Non-'5' Columns
    other_cols = [j for j in range(cols) if j not in five_cols]
    
    non_five_values = []
    for j in other_cols:
      col_values = []
      for i in range(rows):
        if input_grid[i,j] != 0:
          col_values.append(input_grid[i,j])
      if len(col_values) > 0:
        non_five_values.append(col_values)

    # 3. Place Non-'5' Values
    output_col_index = 0
    if len(five_cols) > 0:
      output_col_index = max(five_cols) + 1
    
    for col_values in non_five_values:
      # skip if we have placed all non-five values
      if output_col_index >= cols:
        break

      # find the first available col
      while output_col_index in five_cols:
        output_col_index += 1
        if output_col_index >= cols:
          break

      # place if valid column
      if output_col_index < cols:
        row_index = 0
        for value in col_values:
          if row_index < rows:
            output_grid[row_index, output_col_index] = value
            row_index +=1
        output_col_index += 1


    # 4. Fill Remaining Cells (already done during initialization)

    return output_grid.tolist()
```
