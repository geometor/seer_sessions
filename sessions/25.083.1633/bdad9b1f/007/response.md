```python
"""
1.  **Identify Azure Rows:** Find all rows containing azure (8) pixels.
2.  **Identify Red Rows:** Find all rows containing red (2) pixels.
3.  **Iterate Through Rows:** Process the input grid row by row.
4.  **Copy Non-Red/Azure Rows:** If the current row is *not* a red row and not an azure row, append it directly to the output grid.
5.  **Process Red Rows:** If a row contains red pixels:
      *   Create a copy of the row.
      *   Change *all* red (2) pixels in this copied row to yellow (4).
      * Append this modified row to the output grid
6. **Insert Azure rows:**
      * For each red row, after inserting it (or its modified version) into the output grid, insert copies of the azure rows immediately after it.
      * If no red rows exist, append azure rows to the end.
7. **Output:** The result is the built output grid.
"""

import numpy as np

def find_rows_by_color(grid, color):
    """Finds the indices of rows containing at least one pixel of the specified color."""
    return [i for i, row in enumerate(grid) if np.any(row == color)]

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = []

    # Identify azure and red rows (Steps 1 & 2)
    azure_rows = find_rows_by_color(input_grid, 8)
    red_rows = find_rows_by_color(input_grid, 2)

    # Iterate through rows (Step 3)
    for row_index, row in enumerate(input_grid):
        if row_index not in red_rows and row_index not in azure_rows:
            # Copy non-red/azure rows (Step 4)
            output_grid.append(row.copy())
        elif row_index in red_rows:
            # Process red rows (Step 5)
            transformed_row = row.copy()
            transformed_row[transformed_row == 2] = 4  # Change all red to yellow
            output_grid.append(transformed_row)

            # Insert azure rows after red row (Step 6)
            for azure_row_index in azure_rows:
                output_grid.append(input_grid[azure_row_index].copy())

    # Handle cases with no red rows (append azure rows)
    if not red_rows:
         for azure_row_index in azure_rows:
            output_grid.append(input_grid[azure_row_index].copy())

    return np.array(output_grid)
```