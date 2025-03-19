# 9af7a82c • 014 • example_3 • investigate_coder

---
```python
"""
The transformation takes each column of the input grid, preserves the order of colors, and places these color values in a corresponding output column. The output grid is extended downwards and to the right. Any remaining cells in the output grid that do not have color values from the input are filled with 0 (white). The first column is moved to the leftmost position.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    num_rows_in, num_cols_in = input_grid.shape
    num_rows_out = 5
    num_cols_out = 4
    output_grid = np.zeros((num_rows_out, num_cols_out), dtype=int)

    # Move the first column to the leftmost position.
    output_grid[:num_rows_in, 0] = input_grid[:, 0]

    # Process the remaining columns.
    for j in range(1, num_cols_in):
      output_col_index = j
      input_col = input_grid[:, j]
      
      # Fill output with input and 0
      for i in range(num_rows_out):
          if i < len(input_col):
            output_grid[i, output_col_index] = input_col[i]
          else:
            output_grid[i, output_col_index] = 0


    return output_grid.tolist()
```
