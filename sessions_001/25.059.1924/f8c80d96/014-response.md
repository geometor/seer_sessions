# f8c80d96 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Initialization:** Create an output grid identical in size to the input grid.

2.  **Gray Expansion (White Replacement):** Iterate through each cell in the *input* grid.
    *   If a cell is white (0), change the corresponding cell in the *output* grid to gray (5).

3.  **Border Completion:** Iterate through the *output* grid, rows 0,4,6,8 are changed to all gray (5) and rows 5, 7, and 9 are changed to all red(2) except where the columns are already (2).

4.  **Red Preservation/Copy:** All remaining red pixels are preserved, and all remaining columns that ended in red(2) are changed to red(2).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # White to Gray
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:
                output_grid[r, c] = 5

    # Border Completion and Red Preservation/Copy
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == 4:
                 output_grid[r,c] = 5
            if r == 6 or r == 8:
                output_grid[r] = np.where(output_grid[r] == 0, 5, output_grid[r] )
            if r == 5 or r==7 or r==9:
                output_grid[r] = np.where(output_grid[r] == 0, 2, output_grid[r] )


    return output_grid
```
