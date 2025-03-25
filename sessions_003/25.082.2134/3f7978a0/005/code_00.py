"""
1.  **Identify Target Columns:** Examine each column of the input grid. A column is a "target column" if it *contains* azure (8) and gray (5) pixels, where the non-zero values in the column alternate between 8 and 5. The column can start with either 8 or 5, and 0s are allowed.

2.  **Select Target Columns:** Create a new grid consisting of only the target columns identified in step 1, maintaining their original order.

3.  **Crop Rows:** In the new grid, find the first row and the last row that contain any non-black (non-0) pixels *within the selected columns*. Remove all rows before the first and after the last of these rows.

4.  **Compress Columns:** From the cropped grid, remove any columns that are entirely black (0). The result is the final output grid.
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