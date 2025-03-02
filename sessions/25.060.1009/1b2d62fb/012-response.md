# 1b2d62fb • 012 • refine_coder

---
```python
"""
1.  Examine Input: Inspect the input grid for blue (1) pixels.
2.  Categorize Blue:
    *   If there's a *full* vertical blue line, create an azure segment at row 0, columns 1 and 2 in the output grid.
    *   If there's a *partial* vertical blue line, create an azure segment at row 0, columns 0 and 1.
    * If there is a 2x1 blue rectangle, create an azure segment only at row 0, column 2.
    *   If there are *no* blue pixels, create an azure segment at row 0, columns 1 and 2.
3. Output size: Make the output a 5x3 grid
4.  Fill Remaining:** Fill all other cells in the output grid with white (0).
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
    
def find_blue_rectangle(grid):
    #find 2x1 blue rectangle
    rows, cols = grid.shape
    for i in range(rows -1):
        for j in range(cols):
            if grid[i,j] == 1 and grid[i+1, j] == 1:
                return True
    return False

def transform(input_grid):
    # Initialize output_grid with white (0) and fixed size 5x3.
    output_grid = np.zeros((5, 3), dtype=int)

    # Find the vertical blue (1) line.
    blue_line_col = find_vertical_line(input_grid, 1)
    
    blue_rect = find_blue_rectangle(input_grid)

    # Categorize and create azure segment
    if blue_line_col >= 0 :
        output_grid[0, 1] = 8
        output_grid[0, 2] = 8
    elif blue_line_col == -1:
        output_grid[0,0] = 8
        output_grid[0,1] = 8
    elif blue_rect:
        output_grid[0,2] = 8
    elif blue_line_col == -2:
        output_grid[0,1] = 8
        output_grid[0,2] = 8

    return output_grid
```
