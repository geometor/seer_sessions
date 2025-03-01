# 760b3cac • 006 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all azure (8) and yellow (4) pixels in the input grid.
2.  **Immobile Object:** Yellow (4) pixels do not change their positions. They act as obstacles.
3.  **Mobile Objects:** Azure (8) pixels are mobile.
4. **Transformation:**
    *   Azure (8) pixels move to the leftmost available position within their *own* row.
    *   Yellow (4) pixels block the movement of azure (8) pixels *within a row*.
    *   Azure pixels fill empty spaces to the left within the row, before yellow.
    *  Azure objects stack on the left, occupying the same row as the source row.
"""

import numpy as np

def find_pixels(grid, color):
    # Find coordinates of pixels of the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find azure and yellow pixels.
    azure_pixels = find_pixels(input_grid, 8)
    yellow_pixels = find_pixels(input_grid, 4)

    # Keep yellow pixels unchanged.
    for r, c in yellow_pixels:
        output_grid[r, c] = 4

    # Move azure pixels.
    # clear all azure first
    for r, c in azure_pixels:
      output_grid[r,c] = 0

    # Iterate by row
    for row in range(output_grid.shape[0]):
      # find azure in this row
      azure_in_row = sorted([p for p in azure_pixels if p[0] == row], key=lambda x:x[1])
      # find blocking column, if any
      yellow_in_row = [p[1] for p in yellow_pixels if p[0] == row]
      block_col = min(yellow_in_row) if len(yellow_in_row) > 0 else output_grid.shape[1]

      # place azure
      col = 0
      for a in azure_in_row:
        if col < block_col:
          output_grid[row, col] = 8
          col += 1

    return output_grid
```
