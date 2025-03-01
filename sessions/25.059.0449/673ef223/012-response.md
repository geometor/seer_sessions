# 673ef223 • 012 • refine_coder

---
```python
"""
Transforms an input grid by expanding azure regions from specified seed points to the right,
constrained by red boundaries and grid edges. Additionally, replaces all azure pixels to the right
of yellow pixels with yellow.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the red (2) pixels.
    red_pixels = find_object(input_grid, 2)
    
    # Find azure (8) pixels.
    azure_pixels = find_object(input_grid, 8)

    # 2. & 3. Azure Expansion (both upper and lower)
    for ax, ay in azure_pixels:
        for rx, ry in red_pixels:
            if ax == rx: # same height
                if ay < ry: # red pixel on right
                    for j in range(ay + 1, width):
                        if output_grid[ax, j] == 2:  # stop at red
                            break
                        output_grid[ax, j] = 8
                elif ay > ry: # red pixel on the left
                    for j in range(ay + 1, width):
                        if output_grid[ax,j] == 2:
                            break
                        output_grid[ax,j] = 8
                
    # Find yellow (4) pixels
    yellow_pixels = find_object(input_grid, 4)
        
    # 4. Replacement
    for yx, yy in yellow_pixels:
          for j in range(yy + 1, width):
            if output_grid[yx,j] == 8:
                output_grid[yx,j] = 4
            else: # stop when no more consecutive azure
                break


    return output_grid
```
