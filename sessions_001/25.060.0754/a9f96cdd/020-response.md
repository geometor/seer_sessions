# a9f96cdd • 020 • refine_coder

---
```python
"""
Identifies the top-leftmost non-zero pixel in the input grid, removes it, and conditionally adds azure and orange pixels diagonally below it.
"""

import numpy as np

def find_top_left_nonzero(grid):
    """Finds the top-leftmost non-zero pixel's coordinates."""
    rows, cols = np.nonzero(grid)
    if len(rows) > 0:
        # Find the minimum row index
        min_row = np.min(rows)
        # Find the columns with the minimum row index
        min_cols = cols[rows == min_row]
        # Find the minimum column index among those
        min_col = np.min(min_cols)
        return min_row, min_col
    return None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the top-leftmost non-zero object
    target_location = find_top_left_nonzero(input_grid)

    if target_location:
      row, col = target_location
      
      # Remove the target object
      output_grid[row, col] = 0

      # Conditional addition of azure and orange pixels
      # Place azure pixel one row below and one column to the left, if possible
      if row + 1 < output_grid.shape[0] and col - 1 >= 0 :
          output_grid[row + 1, col - 1] = 8
      # Place orange pixel one row below and one column to the right, if possible
      if row + 1 < output_grid.shape[0] and col + 1 < output_grid.shape[1]:
          output_grid[row + 1, col + 1] = 7

    return output_grid
```
