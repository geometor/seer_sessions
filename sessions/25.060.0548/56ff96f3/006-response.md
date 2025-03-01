# 56ff96f3 • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** all non-white pixels (blue and red) in the input grid.
2.  For each identified pixel:
    *   Create a rectangle of the same color.
    *    Make height = 3
    *   Determine the column index of the original pixel.
    *   Extend the rectangle from column 0 of the input (exclusive) to the initial column, keeping the color constant.
3.  Replace the background with white (0) where there are no colored rectangles.
4. Return the grid.
"""

import numpy as np

def get_non_white_pixels(grid):
    """Finds the coordinates and colors of all non-white pixels."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append(((r, c), grid[r, c]))
    return pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # get all the non-white pixels
    pixels = get_non_white_pixels(input_grid)

    # change output pixels 
    for (row, col), color in pixels:
        # create a 3xN rectangle, where N is the original column index
        # the rectangle starts at column 1 and extends to the initial column (inclusive)
        height = 3
        start_row = row - height // 2
        end_row = row + height // 2 + 1
        
        for r in range(max(0, start_row), min(output_grid.shape[0], end_row)):
            for c in range(0,col+1):
              output_grid[r,c] = color

    return output_grid
```
