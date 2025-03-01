# 2bcee788 • 020 • refine_coder

---
```python
"""
Transforms the input grid by:
1. Changing all background pixels (value 0) to green (value 3).
2. Identifying the contiguous non-zero object (composed of 2s and 7s).
3. Changing all red pixels (value 2) within the object to orange (value 7).
4. Expanding all original orange pixels (value 7) by one cell up and to the right.  Overlapping expansions result in a single pixel.
"""

import numpy as np

def find_object(grid):
    # Find the bounding box of the non-zero elements
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle empty grid
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output_grid with 3s (green)
    output_grid = np.full(input_grid.shape, 3)

    # Find the object's bounding box
    min_row, max_row, min_col, max_col = find_object(input_grid)

    if min_row is not None:  # Proceed only if an object was found
        # Create a copy to track original 7s for expansion.
        original_7s = np.zeros_like(input_grid, dtype=bool)
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 7:
                    original_7s[r, c] = True

        # Iterate through the original object and apply transformations.
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 2:
                    output_grid[r, c] = 7  # Change 2 to 7
                elif input_grid[r,c] == 7:
                    output_grid[r,c] = 7


        # expand the original 7s.
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if original_7s[r, c]:
                    if c + 1 < output_grid.shape[1]:
                        output_grid[r, c + 1] = 7  # Expand right
                    if r - 1 >= 0:
                        output_grid[r - 1, c] = 7  # Expand Up

    return output_grid
```
