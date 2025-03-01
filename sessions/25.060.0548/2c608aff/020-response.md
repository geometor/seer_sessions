# 2c608aff • 020 • refine_coder

---
```python
"""
1.  **Identify the Yellow Object:** Locate the contiguous block of yellow (4) pixels. If there is no yellow object the input does not change.
2.  **Extend with Red:** Add a red (2) pixel to both the left and right side of the yellow object, extending it horizontally. The added pixels should be on the same rows as the yellow pixels. If the yellow object is at the edge of the grid, only add a red pixel to the side that isn't on the edge.
3. All other pixels remain unchanged.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous object of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid_rows = len(input_grid)
    input_grid_cols = len(input_grid[0])

    # Find the yellow object
    yellow_top_left, yellow_bottom_right = find_object(input_grid, 4)
    if yellow_top_left is None:  # No yellow object, return input grid unchanged.
        return output_grid

    # Extend right
    if yellow_bottom_right[1] + 1 < input_grid_cols:
        for i in range(yellow_top_left[0], yellow_bottom_right[0] + 1):
            output_grid[i,yellow_bottom_right[1]+1] = 2

    # Extend Left
    if yellow_top_left[1] -1 >= 0:
      for i in range(yellow_top_left[0], yellow_bottom_right[0] + 1):
          output_grid[i, yellow_top_left[1] - 1] = 2

    return output_grid
```
