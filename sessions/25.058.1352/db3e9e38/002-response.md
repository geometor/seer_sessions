# db3e9e38 • 002 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the Object:** Find the vertical line of orange (7) pixels. Note its height and starting column.
2.  **Add/Transform:**
    *   Iterate through the original orange line from top to bottom. For each orange pixel: Add an azure (8) pixel above it.
    *   If the orange (7) is not on an edge (left or right boundary), add an azure (8) to the left and to the right.
    *   If the orange (7) pixel is at the left edge of grid, add a '7' to its left.
    *   If the orange (7) pixel is on the right edge, add a '7' to its right.
3. Fill background: keep all other pixels to '0'.
"""

import numpy as np

def find_vertical_line(grid, color=7):
    """Finds the starting row, column, and height of a vertical line of a given color."""
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                # Found the start, now find the end
                start_row = r
                start_col = c
                height = 0
                while r < rows and grid[r, c] == color:
                    height += 1
                    r += 1
                return start_row, start_col, height
    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros_like(input_grid)
    start_row, start_col, height = find_vertical_line(input_grid)

    if start_row is None:  # No vertical line found, return empty grid
        return output_grid

    for i in range(height):
        current_row = start_row + i
        current_col = start_col

        # Add 8 above
        if current_row > 0:
          output_grid[current_row - 1, current_col] = 8

        # Add 8 to left and right if not on edge
        if current_col > 0:
          if current_row > 0:
            output_grid[current_row - 1, current_col-1] = 8
        if current_col < output_grid.shape[1] - 1:
           if current_row > 0:
            output_grid[current_row - 1, current_col + 1] = 8


        #handle current row
        output_grid[current_row,current_col] = 7

        # handle edge cases for 7
        if current_col == 0 :
           output_grid[current_row,current_col] = 7
        if current_col == output_grid.shape[1]-1:
           output_grid[current_row,current_col] = 7

    return output_grid
```
