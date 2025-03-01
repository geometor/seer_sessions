# 2dee498d • 010 • refine_coder

---
```python
"""
The input grid is transformed into the output grid by keeping only the columns that contain the color black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as an empty list.
    output_grid = []

    # Get the number of rows and columns in the input grid.
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Find columns that contain black (0).
    cols_to_keep = []
    for col_index in range(num_cols):
        for row_index in range(num_rows):
            if input_grid[row_index][col_index] == 0:
                cols_to_keep.append(col_index)
                break  # Move to the next column once black is found

    # Construct the output grid with only the selected columns.
    for row_index in range(num_rows):
        new_row = []
        for col_index in cols_to_keep:
            new_row.append(input_grid[row_index][col_index])
        output_grid.append(new_row)

    return output_grid
```

