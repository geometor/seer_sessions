# bc1d5164 • 028 • example_5 • investigate_coder

---
```python
"""
1.  **Identify Target Rows and Columns**: Examine the input grid to identify all rows and columns that contain at least one cell with the value '3' (green).
2.  **Extract Sub-grid**: Create a new grid (the output grid).
3. Populate output grid: The output grid consists exclusively out of intersecting cells of the previously identified rows and columns.
"""

import numpy as np

def get_target_indices(input_grid):
    """Finds rows and columns containing non-zero values."""
    rows = []
    cols = []
    for i, row in enumerate(input_grid):
        if any(val != 0 for val in row):
            rows.append(i)
    for j in range(input_grid.shape[1]):
        if any(input_grid[i][j] != 0 for i in range(input_grid.shape[0])):
            cols.append(j)
    return rows, cols


def transform(input_grid):
    """Extracts the subgrid containing all non-zero values."""
    
    input_grid = np.array(input_grid)
    
    # Identify target rows and columns.
    target_rows, target_cols = get_target_indices(input_grid)
    
    # Extract subgrid
    output_grid = input_grid[np.ix_(target_rows, target_cols)]

    return output_grid.tolist()
```
