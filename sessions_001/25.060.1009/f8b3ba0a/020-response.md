# f8b3ba0a • 020 • refine_coder

---
```python
"""
1. Examine Rows: Iterate through each row of the input grid.
2. Check for Non-White Pixels: For each row, determine if it contains at least one pixel that is not white (value 0).
3. Conditional Selection: If a row contains any non-white pixels, select it.
4. Construct Output: Create the output grid by stacking the selected rows vertically, preserving their original order.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # Initialize an empty list to hold the selected rows
    output_rows = []

    # Iterate through each row of the grid
    for row in grid:
        # Check if the row contains any non-white pixels (non-zero values)
        if np.any(row != 0):
            # Add the row to the output_rows list
            output_rows.append(row)

    # Convert the list of rows to a NumPy array. If output_rows is empty, this will
    # result in an array with shape (0,).  We need to handle this case to ensure
    # the output grid has the correct dimensions even when no rows are selected.
    if output_rows:
        output_grid = np.array(output_rows)
    else:
        # If no rows are selected, return an empty array with the correct number of columns.
        # We infer this from the input grid.  If the input_grid is empty, return an empty array.
        if grid.size == 0:
            return np.array([])        
        output_grid = np.empty((0, grid.shape[1]), dtype=int)

    return output_grid
```
