```python
"""
Copies a column with non-zero values from the input grid to the output grid, while setting all other cells in the output grid to zero. The specific column to copy is determined by finding a column that contains non-zero values.
"""

import numpy as np

def find_non_zero_column(grid):
    # Iterate through columns and return the index of the first column found
    # with at least one non-zero value
    num_cols = grid.shape[1]
    for col_index in range(num_cols):
        if np.any(grid[:, col_index] != 0):
            return col_index
    return None # no non-zero columns

def transform(input_grid):
    # Initialize an output grid with the same dimensions as the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # Find the index of the first non-zero column.
    target_column_index = find_non_zero_column(input_grid)
    
    if target_column_index is not None:
      # Copy the values from the target column of the input grid to the output grid.
      output_grid[:, target_column_index] = input_grid[:, target_column_index]

    return output_grid
```