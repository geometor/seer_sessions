# 834ec97d • 006 • refine_coder

---
```python
"""
1.  Identify the single red pixel (value 2) in the input grid.
2.  If the red pixel is NOT in the last row, move the red pixel down by one row, and place a yellow pixel (value 4) in the original position of the red pixel.
3.  If the red pixel IS in the last row, it stays in the same place. Place a yellow pixel (value 4) in the position immediately above the red pixel, if such a position exists.
4. All other cells remain 0.
"""

import numpy as np

def find_pixel_by_color(grid, color_value):
    # Find the coordinates of a pixel with the specified color value.
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:
        return [coords[0][0], coords[1][0]]  # return first occurance
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the red pixel (value 2).
    red_pixel_pos = find_pixel_by_color(input_grid, 2)

    # Move the red pixel down by one row, or keep in place if at the bottom.
    if red_pixel_pos:
        if red_pixel_pos[0] < input_grid.shape[0] - 1:
            new_red_pos = [red_pixel_pos[0] + 1, red_pixel_pos[1]]
            output_grid[new_red_pos[0], new_red_pos[1]] = 2  # move down
            output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 4 # yellow in old place
        else:
            output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 2 # stay in old place
            if red_pixel_pos[0] > 0:
                output_grid[red_pixel_pos[0]-1, red_pixel_pos[1]] = 4 # yellow above


    return output_grid
```

