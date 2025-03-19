# 10fcaaa3 • 006 • refine_coder

---
```python
"""
1. **Duplicate Rows:** Duplicate each row of the input grid. This doubles the height of the grid.

2.  **Identify Gray Column:** Find the column in the *original* input grid that contains gray (5) pixels.

3.  **Expand Columns:**
    *   In the duplicated-row grid, duplicate the column that *corresponded* to the gray column in the *original* input. Insert this duplicate immediately to the right of the original.

4.  **Add Azure Rows:** Add a row above and below the resulting grid. These rows consist of alternating azure (8) and white (0) pixels, beginning with azure.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Rows
    duplicated_rows_grid = np.repeat(input_grid, 2, axis=0)

    # Find the column index with gray (5) in the original input
    gray_col_indices = np.where(input_grid == 5)[1]
    gray_col_index = gray_col_indices[0] if len(gray_col_indices) > 0 else -1

    # Expand Columns
    output_grid_cols = []
    for col_idx in range(duplicated_rows_grid.shape[1]):
        output_grid_cols.append(duplicated_rows_grid[:, col_idx])
        if col_idx == gray_col_index:
            output_grid_cols.append(duplicated_rows_grid[:, col_idx])  # Duplicate gray column

    expanded_grid = np.column_stack(output_grid_cols)

    # Add Azure Rows
    azure_row = np.array([8 if i % 2 == 0 else 0 for i in range(expanded_grid.shape[1])])
    output_grid = np.vstack([azure_row, expanded_grid, azure_row])

    return output_grid
```

