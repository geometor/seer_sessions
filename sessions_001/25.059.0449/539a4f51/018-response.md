# 539a4f51 • 018 • example_3 • investigate_coder

---
```python
"""
The input grid is duplicated and placed side-by-side. Then, additional rows are appended to the bottom, 
mirroring the color sequence of the columns in the original grid, to form a 10x10 output grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid.
    input_grid = np.array(input_grid)
    duplicated_grid = np.copy(input_grid)

    # Combine the original and duplicated grids horizontally.
    output_grid = np.concatenate((input_grid, duplicated_grid), axis=1)

    # Get the number of rows and columns in the combined grid
    num_rows, num_cols = output_grid.shape
    
    # Get original input_grid size
    in_rows, in_cols = input_grid.shape

    # Append rows
    new_rows = []
    for i in range(in_rows):
      row = []
      for j in range(in_cols):
        row.append(input_grid[i,j])
      for j in range(in_cols):
        row.append(input_grid[i,j])
      new_rows.append(row)

    new_rows = np.array(new_rows)

    output_grid = np.concatenate((output_grid, new_rows), axis=0)

    return output_grid.tolist()
```
