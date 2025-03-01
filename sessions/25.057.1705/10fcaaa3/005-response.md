# 10fcaaa3 • 005 • refine_coder

---
```python
"""
Duplicates input rows, adds alternating azure/blank rows at the top and bottom, and expands columns.  The column expansion inserts blank columns around each original column, with special handling for columns containing gray (5): the gray column is repeated three times without blanks.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Input Rows
    intermediate_grid = np.repeat(input_grid, 2, axis=0)

    # Find the column index with gray (5)
    gray_col_indices = np.where(input_grid == 5)[1]
    gray_col_index = gray_col_indices[0] if len(gray_col_indices) > 0 else -1

    # Expand and Duplicate Columns based on Gray
    output_grid_cols = []
    for col_idx in range(intermediate_grid.shape[1]):
        if col_idx == gray_col_index:
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(intermediate_grid[:, col_idx])

        else:
            output_grid_cols.append(np.zeros(intermediate_grid.shape[0],dtype=int))
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(np.zeros(intermediate_grid.shape[0],dtype=int))

    intermediate_grid = np.column_stack(output_grid_cols)


    # remove the extra columns
    output_grid = intermediate_grid[:,1:intermediate_grid.shape[1]-1]


    # Add Azure Rows
    azure_row = np.array([8 if i % 2 == 0 else 0 for i in range(output_grid.shape[1])])
    output_grid = np.vstack([azure_row, output_grid, azure_row])

    return output_grid
```
