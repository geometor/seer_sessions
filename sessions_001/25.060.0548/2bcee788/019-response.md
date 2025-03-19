# 2bcee788 • 019 • refine_coder

---
```python
"""
1.  **Identify the Input Object:** Find the bounding box of the contiguous non-zero region within the input grid. This defines the primary object.
2.  **Default Background:** Initialize the output grid to green (3).
3.  **Transform Input Pixels:**
    *   All pixels that are red (2) in the input object should become orange (7) in the output.
    *   All orange pixels (7) in the input should become orange (7) in the output.
4.  **Apply Expansion:** If any pixel within the input object's bounding box has the value orange (7), add orange pixels (7) in the output grid at one pixel to the right of that orange pixel and one pixel up from that pixel. These locations may be outside of the identified input object.
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
        # Iterate through the original object and apply transformations.
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 2:
                    # replace with 7, no expansion.
                    output_grid[r,c] = 7
                elif input_grid[r, c] == 7:
                    output_grid[r, c] = 7  # keep original 7
                    if c + 1 < output_grid.shape[1]:
                        output_grid[r, c + 1] = 7  # Expand right
                    if r -1 >= 0:
                        output_grid[r - 1, c] = 7 # Expand Up.
    return output_grid
```
