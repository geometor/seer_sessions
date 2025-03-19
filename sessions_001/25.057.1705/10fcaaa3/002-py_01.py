"""
The transformation rule can be described as follows:

1. **Duplicate Input Rows:** The input grid's rows are duplicated to create an intermediate grid that is twice the height of the input.
2. **Expand and Duplicate Columns based on Gray:**
   - Locate the column in the original input containing gray (5) pixels.
   - Duplicate columns in the intermediate grid. The columns containing gray cells are duplicated to the left and right, maintaining the gray cells in the copied column. All the other columns just have 0 added to the right and left.
3. **Add Azure Rows:** Add a row above and a row below the current intermediate grid. These rows consist of alternating azure (8) and white (0) pixels, starting with azure.
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