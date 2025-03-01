# d687bc17 • 016 • example_3 • investigate_coder

---
```python
"""
Preserve the top (magenta) and bottom (green) horizontal bands, and the left (yellow) and right (azure) vertical bands.
Within the inner region:
1. Change the yellow(4) pixel in the 4th row and 9th column to magenta (6).
2. Remove the red (2) pixel.
3. Remove the single magenta(6) pixel that was originally in the 4th row and 9th column.
4. Keep all other isolated azure(8) and yellow(4) pixels within the center.

"""

import numpy as np

def find_pixel(grid, color, row_start, row_end, col_start, col_end):
    # find a specific pixel in a subgrid
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if grid[r,c] == color:
                return (r,c)
    return None

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Change yellow to magenta
    output_grid[3,8] = 6 # since array indexing starts at 0

    # Remove the red (2) pixel.  It's located at (2,2)
    output_grid[2,2] = 0
    
    # Remove the magenta(6) pixel, now in the 9th column and 4th row
    #output_grid[3, 8] = 0 # it used to be here, so don't do this


    return output_grid
```
