```python
"""
1.  **Identify Target Columns:** Iterate through each column of the input grid. A column is considered a "target column" if it contains only the values 8 (azure), 5 (gray), and 0 (black), and the non-zero values within the column strictly alternate between 8 and 5. The alternation can start with either 8 or 5.
2.  **Select Target Columns:** Create a new grid containing only the target columns identified in the previous step. Maintain the original order of these columns.
3.  **Crop Rows:** Examine the new grid formed by the selected target columns. Find the indices of the first and last rows that contain any non-zero values. Remove all rows before the first non-zero row and all rows after the last non-zero row.
4.  **Compress Columns:** From the cropped grid, remove any columns that consist entirely of zeros. The resulting grid is the final output.
"""

import numpy as np

def _is_target_column(column):
    """Checks if a column contains alternating 8s and 5s (can contain 0s)."""
    non_zero_elements = [x for x in column if x != 0]
    if not all(x in [5, 8] for x in non_zero_elements):
        return False
    for i in range(len(non_zero_elements) - 1):
        if non_zero_elements[i] == non_zero_elements[i+1]:
            return False
    return len(non_zero_elements) > 0

def _crop_rows(grid):
    """Removes top and bottom rows that are all zeros within selected columns."""
    if grid.size == 0:  # Handle empty grid
        return grid
    rows_with_content = [i for i in range(grid.shape[0]) if not np.all(grid[i,:] == 0)]
    if not rows_with_content:
        return np.zeros((0, grid.shape[1]), dtype=int)
    first_row = rows_with_content[0]
    last_row = rows_with_content[-1]
    return grid[first_row:last_row+1, :]

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Target Columns
    num_cols = input_grid.shape[1]
    target_column_indices = []
    for j in range(num_cols):
        if _is_target_column(input_grid[:, j]):
            target_column_indices.append(j)

    # 2. Select Target Columns
    selected_grid = input_grid[:, target_column_indices]

    # 3. Crop Rows
    cropped_grid = _crop_rows(selected_grid)

    # 4. Compress Columns (remove all-zero columns)
    if cropped_grid.size == 0:  # Handle empty grid
        output_grid = np.zeros((0, 0), dtype=int)
    else:
       compressed_columns = []
       for j in range(cropped_grid.shape[1]):
          if not np.all(cropped_grid[:,j] == 0):
            compressed_columns.append(cropped_grid[:,j])

       if (len(compressed_columns) > 0):
           output_grid = np.stack(compressed_columns, axis=1)
       else:
           output_grid = np.zeros((0,0), dtype=int)


    return output_grid.tolist()
```