# 67a423a3 • 004 • example_1 • investigate_coder

---
```python
"""
White pixels become Yellow unless there is a green pixel above
or below or a yellow pixel to the sides.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # preservation of non-white pixel
            if input_grid[r, c] != 0:
                continue

            # conditional change for white pixels
            is_above_green = (r > 0 and input_grid[r-1, c] == 3)
            is_below_green = (r < rows - 1 and input_grid[r+1, c] == 3)
            is_adjacent_yellow = False

            if c > 0 and output_grid[r,c-1] == 4:
                is_adjacent_yellow = True
            if r > 0 and output_grid[r-1,c] == 4:
                is_adjacent_yellow = True    
            if c < cols -1 and output_grid[r,c+1] == 4:
                is_adjacent_yellow = True
            if r < rows - 1 and output_grid[r+1, c] == 4:
                is_adjacent_yellow = True
            
            if not (is_above_green or is_below_green or is_adjacent_yellow):
                 output_grid[r, c] = 4

    return output_grid
```
