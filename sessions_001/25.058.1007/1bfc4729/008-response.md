# 1bfc4729 • 008 • refine_coder

---
```python
"""
1.  Identify Non-Zero Pixels: Locate all pixels in the input grid that have a non-zero value.
2.  Conditional Expansion:
    *   If a non-zero pixel is the only non-zero pixel in its row, expand it *vertically* into a line of the same color, covering the entire column.  Then set original pixel to zero.
    *   If a non-zero pixel is the only non-zero pixel in its column, expand it *horizontally* into a line of the same color, covering the entire row. Then set original pixel to zero.
    *    If a non-zero pixel is the only non-zero pixel in both its row and its column, do *nothing*. Then set original pixel to zero.
    * If there is more than one non-zero pixel in its row *and* its column - do nothing, but keep the original pixel.
3. Output the result.
"""

import numpy as np

def count_non_zero_in_row(grid, row):
    """Counts non-zero pixels in a given row."""
    return np.count_nonzero(grid[row, :])

def count_non_zero_in_column(grid, col):
    """Counts non-zero pixels in a given column."""
    return np.count_nonzero(grid[:, col])

def transform(input_grid):
    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the input_grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                value = input_grid[r, c]
                # Check if it's the only non-zero pixel in its row and column
                if count_non_zero_in_row(input_grid, r) == 1 and count_non_zero_in_column(input_grid,c) == 1:
                  output_grid[r,c] = 0
                # Check if it's the only non-zero pixel in its row
                elif count_non_zero_in_row(input_grid, r) == 1:
                    # Expand vertically
                    for i in range(rows):
                        output_grid[i, c] = value
                # Check if it's the only non-zero pixel in its column
                elif count_non_zero_in_column(input_grid, c) == 1:
                    # Expand horizontally
                    for i in range(cols):
                        output_grid[r, i] = value
                else: # Added condition where pixel exists
                    output_grid[r,c] = value


    return output_grid
```
