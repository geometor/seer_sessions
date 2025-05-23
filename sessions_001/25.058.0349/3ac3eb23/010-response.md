# 3ac3eb23 • 010 • refine_coder

---
```python
"""
1.  **Locate:** Find the single yellow (4) pixel in the input grid.
2.  **Mirror:** From the found position, copy it on the immediate right neighbor, if the neighbor is 0.
3.  **Propagate:** From the found position, draw a vertical line downwards to the bottom of the grid, copying the yellow pixel.
4. Mirror: From each newly generated pixel, copy it on the immediate right neighbor, if neighbor is 0.
5. all other are unchanged.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find the yellow pixel (4)
    yellow_pixel_coords = find_pixel(input_grid, 4)
    
    if yellow_pixel_coords:
        y, x = yellow_pixel_coords

        # mirror initial yellow pixel, if not out of bounds
        if (x + 1) < output_grid.shape[1] and output_grid[y, x+1] == 0:
          output_grid[y,x+1] = 4

        # Propagate downwards, copying the yellow pixel
        for i in range(y + 1, output_grid.shape[0]):
            output_grid[i, x] = 4  # Yellow
            
            # mirror each newly propogated pixel
            if (x + 1) < output_grid.shape[1] and output_grid[i,x+1] == 0:
              output_grid[i, x + 1] = output_grid[i,x]

    return output_grid
```
