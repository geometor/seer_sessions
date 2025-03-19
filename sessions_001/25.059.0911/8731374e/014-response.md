# 8731374e • 014 • refine_coder

---
```python
"""
1.  **Identify the Subgrid:** Find the smallest rectangular region within the input grid that contains all non-zero pixels. This is the subgrid.

2.  **Output Grid:** Create an output grid of the *same dimensions* as the input grid, filled with zeros.

3.  **Process Subgrid:** Within the subgrid:
    *   **Color Transformation:**
        *   If an input pixel within the subgrid is yellow (4), copy its value to the corresponding position in the output grid.
        *   If an input pixel within the subgrid is any other non-zero color, set the corresponding output pixel to blue (1).

    *   **Column-Based Patterning:**
        *   **Even Columns:** For all even-numbered columns (starting the count from 1) within the subgrid, set all pixels in the corresponding output grid location to blue (1).
        *   **Odd Columns:** For all odd-numbered columns (starting the count from 1) within the subgrid, set every third, starting with the third, pixel in that output grid location to blue(1)

4.  **Outside Subgrid:** Pixels in the output grid that fall outside the subgrid remain zero (white).
"""

import numpy as np

def _find_subgrid(grid):
    """Finds the bounding box of non-zero pixels."""
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Identify the Subgrid
    min_row, max_row, min_col, max_col = _find_subgrid(input_grid)

    # 3. Process Subgrid
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            # Color Transformation
            if input_grid[r, c] == 4:
                output_grid[r, c] = 4
            elif input_grid[r, c] != 0:
                output_grid[r, c] = 1

            # Column-Based Patterning
            if (c - min_col + 1) % 2 == 0:  # Even column within subgrid
                output_grid[r, c] = 1
            elif (r - min_row) % 3 == 2:   # every third starting from the third row (index 2)
                output_grid[r,c] = 1

    return output_grid
```
