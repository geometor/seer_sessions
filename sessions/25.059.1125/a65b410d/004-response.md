# a65b410d • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** all pixels with the value '2' (red) in the input grid.
2.  **For each** red pixel:
    *   Create a green '3' pixel directly above, as long as it exists within the output grid. Continue expanding upwards adding green '3' until reaching the grid boundary, forming a contiguous green object expanding diagonally to the upper left and upper right.
    *   Create a blue '1' pixel directly below the left-most '2' if it exists.
3.  **Retain** all original '2' pixels in their original position.
4.  All other pixels that were '0' (white) in the input grid remain '0' (white).
"""

import numpy as np

def get_red_pixels(grid):
    # Find coordinates of all red pixels (value 2).
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 2:
                red_pixels.append((r,c))
    return red_pixels

def transform(input_grid):
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    if not red_pixels:
        return input_grid # handles the case where there are no red pixels.

    for r, c in red_pixels:
      # grow green upwards
      for i in range(r -1, -1, -1):
        if c + (r-1-i) < output_grid.shape[1]:
           output_grid[i,min(c + (r-1-i),output_grid.shape[1] - 1)] = 3
        if c - (r-1-i) >= 0:
           output_grid[i,max(c - (r-1-i), 0)] = 3

    # grow blue downwards
    leftmost_red_x = min(red_pixels, key=lambda item: item[1])[0]
    if leftmost_red_x + 1 < output_grid.shape[0]:
       output_grid[leftmost_red_x + 1, min(red_pixels, key=lambda item: item[1])[1] ] = 1
    
    return output_grid
```
