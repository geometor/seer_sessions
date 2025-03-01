# 5bd6f4ac • 017 • refine_coder

---
```python
"""
1.  **Identify and remove empty rows:** Scan the input grid from top to bottom. If a row contains only white pixels (0), and no non-white pixels mark it for removal.
2.  **Identify and Remove empty columns:** Scan the input grid from left to right. If a column contains only white pixels (0) and no non-white pixels, mark it for removal.
3.  **Create Output:** Create a new grid. Successively add rows from the original grid, starting at the top, as long as they haven't been marked for removal.  Do the same for columns, adding from left to right.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    input_grid = np.array(input_grid)  # Ensure numpy array
    rows, cols = input_grid.shape

    # Identify non-empty rows and columns
    non_empty_rows = []
    for i in range(rows):
        if np.any(input_grid[i] != 0):
            non_empty_rows.append(i)

    non_empty_cols = []
    for j in range(cols):
        if np.any(input_grid[:, j] != 0):
            non_empty_cols.append(j)

    # Determine rows and cols to keep
    rows_to_keep = non_empty_rows
    cols_to_keep = non_empty_cols


    # Build the output grid
    if not rows_to_keep or not cols_to_keep:  # Handle empty output
        output_grid = np.array([])
    else:
        # Use numpy array slicing for efficient subgrid extraction
        output_grid = input_grid[np.ix_(rows_to_keep, cols_to_keep)]

    return output_grid.tolist()
```
