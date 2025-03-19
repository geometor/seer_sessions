# 1f0c79e5 • 022 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the Core:** Locate the 2x2 block of pixels in the center of the input grid, including three red(2) and one orange(7).
2.  **Isolate Key Pixel:** Determine the position of color 7 within the core 2x2 block.
3.  **Pattern Generation:** Fill the output grid with the orange color (7) according to this rule:
    *   Fill three continuous pixels with orange from the top left corner toward right and bottom side.
    *   Then add four more orange pixels from the ending point of each orange stripe by creating another adjacent line.
    *  Finally, fill one line from the end of each "L" shaped orange area.
    *   Leave remaining pixels white.
"""

import numpy as np

def find_2x2_block(grid):
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] != 0 and grid[r+1, c] !=0 and grid[r,c+1] != 0 and grid[r+1, c+1] != 0:
               return r, c
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # find 2x2 block and orange pixel position.
    start_row, start_col = find_2x2_block(input_grid)
    
    # Fill the output according to the orange position

    # Fill three pixels toward right and bottom
    for i in range(3):
        if start_row + i < rows:
          output_grid[start_row + i, 0] = 7
        if start_col + i < cols:
            output_grid[0, start_col + i] = 7
    
    # Add four more orange from the last position of each orange line
    for i in range(4):
      if start_row+2+i < rows:
        output_grid[start_row + 2+i, 1] = 7
      if start_col+2+i < cols:
        output_grid[1,start_col+2+i] = 7

    # fill the last line from L shape
    output_grid[start_row + 6, 0] = 7
    output_grid[0,start_col+6] = 7
    output_grid[1,start_col+6] = 7
    
    return output_grid
```
