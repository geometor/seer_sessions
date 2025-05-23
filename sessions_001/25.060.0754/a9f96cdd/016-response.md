# a9f96cdd • 016 • example_3 • investigate_coder

---
```python
"""
Locates a single non-zero pixel in the input grid, removes it, and places two new pixels (azure and orange) diagonally below it to the left and right, respectively.
"""

import numpy as np

def find_object(grid):
    # Find the indices of the non-zero element
    rows, cols = np.nonzero(grid)
    if len(rows) == 1:  # Ensure there's only one non-zero element
        return rows[0], cols[0]
    else:
        return None  # Handle cases where there isn't exactly one object

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the non-zero object
    object_location = find_object(input_grid)

    if object_location:
      row, col = object_location
      
      # Remove the original object
      output_grid[row, col] = 0

      # Create and place the new azure pixel (8)
      new_row = row + 1
      new_col_left = col - 1
      if 0 <= new_row < output_grid.shape[0] and 0 <= new_col_left < output_grid.shape[1]:
          output_grid[new_row, new_col_left] = 8

      # Create and place the new orange pixel (7)
      new_col_right = col + 1
      if 0 <= new_row < output_grid.shape[0] and 0 <= new_col_right < output_grid.shape[1]:
          output_grid[new_row, new_col_right] = 7

    return output_grid
```

