```python
"""
1.  **Iterate** through each pixel of the input grid.
2.  **Identify** yellow (4) pixels.
3. **Conditional Transformation:** For each yellow pixel, replace with an orange (7) if certain adjacency conditions are met, as follows.
    *   If a yellow pixel is part of a contiguous 3x1 or 1x3 block of yellow pixels, change the center pixel of the yellow block to orange.
    *   If a yellow pixel is a corner in an L shape block of 3 pixels, change the corner pixel to orange.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    def is_yellow(pixel):
        return pixel == 4

    def check_3x1(grid, i, j):
      # check for a 3x1 yellow block centered at i,j
        if j > 0 and j < grid.shape[1] - 1:
            if (is_yellow(grid[i, j-1]) and
                is_yellow(grid[i, j]) and
                is_yellow(grid[i, j+1])):
                return True
        return False

    def check_1x3(grid, i, j):
      # check for a 1x3 yellow block centered at i,j
        if i > 0 and i < grid.shape[0] - 1:
            if (is_yellow(grid[i-1, j]) and
                is_yellow(grid[i, j]) and
                is_yellow(grid[i+1, j])):
                return True
        return False
    
    def check_L_shape(grid, i, j):
      # check four possible L shapes, change corner to orange
        if i > 0 and j > 0: # top-left corner
            if is_yellow(grid[i-1,j]) and is_yellow(grid[i,j-1]): return True
        if i > 0 and j < grid.shape[1] - 1: # top-right
            if is_yellow(grid[i-1,j]) and is_yellow(grid[i,j+1]): return True
        if i < grid.shape[0] - 1 and j > 0: # bottom-left
            if is_yellow(grid[i+1,j]) and is_yellow(grid[i,j-1]): return True
        if i < grid.shape[0] - 1 and j < grid.shape[1] - 1: #bottom-right
            if is_yellow(grid[i+1,j]) and is_yellow(grid[i,j+1]): return True
        return False
            

    # change output pixels
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if is_yellow(output_grid[i,j]):
                if check_3x1(output_grid, i, j) or check_1x3(output_grid, i, j) or check_L_shape(output_grid,i,j):
                    output_grid[i,j] = 7

    return output_grid
```