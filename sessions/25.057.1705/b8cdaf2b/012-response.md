# b8cdaf2b • 012 • refine_coder

---
```python
"""
1.  **Preserve Background:** Copy the bottom two rows of the input grid directly to the output grid.
2.  **Determine Number of Rows to Insert:** The number of rows to insert is equal to the height of the input grid minus 2.
3. **Construct Inserted Rows:**
   *   Iteratively create new rows, starting with green (3) at opposite ends of the row and filling the rest with white (0).
   *    For each subsequent row, move the green pixels one position closer to the center.
   *   Stop when either the green pixels would overlap, or the number of rows to create is met.
4.  **Combine:** Insert the constructed rows at the top of the output grid.
"""

import numpy as np

def _construct_inserted_row(cols, offset):
    """Helper function to construct a single inserted row."""
    row = np.zeros(cols, dtype=int)
    if offset < cols // 2:  # Ensure green pixels don't overlap
        row[offset] = 3
        row[cols - 1 - offset] = 3
    return row

def transform(input_grid):
    # Initialize the output grid 
    output_grid = np.copy(input_grid)
    
    # Get dimensions of the input grid
    rows, cols = input_grid.shape
    
    # Determine the number of rows to insert
    num_rows_to_insert = rows - 2
    
    # Construct inserted rows
    inserted_rows = []
    for i in range(num_rows_to_insert):
        row = _construct_inserted_row(cols, i)
        inserted_rows.append(row)

    # build output grid from constructed rows and bottom two rows
    output_grid = np.vstack((*inserted_rows, input_grid[-2:,:]))

    return output_grid
```
