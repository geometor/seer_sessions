# a65b410d • 008 • refine_coder

---
```python
"""
1.  **Identify** all red ('2') pixels in the input grid.
2.  **For each** red pixel:
    *   Create a green ('3') pixel in the cell directly above the red pixel, if that cell is within the grid.  Continue creating green pixels upwards in a straight vertical line until the top edge of the grid is reached.
3.  **Find** the *top-most* red pixel. If there are multiple red pixels in the top-most row, select any one of them.
4.  Create one blue ('1') pixel one column *to the left* of this top-most red pixel.
    *  If the top-most red pixel is already in the first column (column 0), then do *not* create a blue pixel.
5.  **Retain** all original red pixels in their original positions.
6.  All other pixels that were '0' (white) in the input grid remain '0' (white).
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

def get_topmost_red_pixel(red_pixels):
    # find the top-most red pixel
    if not red_pixels:
        return None
    return min(red_pixels, key=lambda item: item[0])

def transform(input_grid):
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    if not red_pixels:
        return input_grid # handles the case where there are no red pixels.

    for r, c in red_pixels:
      # grow green upwards
      for i in range(r -1, -1, -1):
        output_grid[i,c] = 3

    # grow blue to the left of top-most red
    topmost_red_pixel = get_topmost_red_pixel(red_pixels)
    topmost_red_row, topmost_red_col = topmost_red_pixel

    if topmost_red_col > 0:
       output_grid[topmost_red_row, topmost_red_col - 1] = 1
    
    return output_grid
```

