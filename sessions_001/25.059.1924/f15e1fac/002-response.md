# f15e1fac • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves repositioning azure (8) pixels based on their initial row/column presence while preserving red (2) pixels in the bottom row. Azure pixels in the input, if present in a column, are copied to an output column, maintaining their count. Similarly, azure pixels in an input row are copied to an output row. Red pixels are always maintained on the bottom row.
"""

import numpy as np

def get_azure_positions(grid):
    """Finds the row and column indices of azure (8) pixels."""
    azure_rows = []
    azure_cols = []
    for i, row in enumerate(grid):
        if 8 in row:
            azure_rows.append((i, [j for j, val in enumerate(row) if val == 8]))
    for j in range(grid.shape[1]):
        col = grid[:, j]
        if 8 in col:
            azure_cols.append((j, [i for i, val in enumerate(col) if val == 8]))
    return azure_rows, azure_cols

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Get azure positions
    azure_rows, azure_cols = get_azure_positions(input_grid)

    # Transform azure pixels based on column presence.
    for col, rows in azure_cols:
        for row_index in rows:
             output_grid[row_index][col] = 8


    # Transform azure pixels based on row presence.
    for row, cols in azure_rows:
        for col_index in cols:
            output_grid[row][col_index] = 8


    # Preserve red pixels in the bottom row.
    for i, val in enumerate(input_grid[-1]):
        if val == 2:
            output_grid[-1, i] = 2

    return output_grid.tolist()
```
