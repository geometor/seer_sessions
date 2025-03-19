# 1b2d62fb • 014 • refine_coder

---
```python
"""
1.  **Input:** Examine the input grid.
2.  **Output Size:** Create an output grid of size 5x3.
3.  **Blue Check:**
    *   If there's a *full* vertical blue line (all rows in a column are blue) or *no* blue pixels, create an azure segment at row 0, columns 1 and 2 of the output grid.
    *   If there's a *partial* vertical blue line (at least one, but not all, rows in a column are blue) *or* if there are *any* blue pixels, create an azure segment at row 0, columns 0 and 1 of the output grid.
4.  **Fill Remaining:** Fill all other cells in the output grid with white (0).
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the column index where the vertical line of the specified color exists.
    # Return -1 for partial lines, -2 for no lines, and the column index for full lines.
    rows, cols = grid.shape
    for j in range(cols):
        is_line = True
        is_partial = False
        for i in range(rows):
            if grid[i, j] != color:
                if np.any(grid[:,j] == color):
                     is_partial = True
                is_line = False
                
        if is_line:
            return j
    if is_partial:
        return -1
    return -2
    
def any_blue_pixels(grid):
    #check for any blue pixels
    return np.any(grid == 1)

def transform(input_grid):
    # Initialize output_grid with white (0) and fixed size 5x3.
    output_grid = np.zeros((5, 3), dtype=int)

    # Find the vertical blue (1) line.
    blue_line_col = find_vertical_line(input_grid, 1)
    
    # Check for any blue
    blue_pixels = any_blue_pixels(input_grid)

    # Categorize and create azure segment
    if blue_line_col >= 0 or blue_line_col == -2:
        output_grid[0, 1] = 8
        output_grid[0, 2] = 8
    elif blue_line_col == -1 or blue_pixels:
        output_grid[0,0] = 8
        output_grid[0,1] = 8

    return output_grid
```
