# 40853293 • 002 • example_2 • investigate_coder

---
```python
"""
Transforms single pixels in the input grid into centered horizontal and vertical lines of the same color in the output grid.
Lines extend to include adjacent diagonal pixels of the same color.
"""

import numpy as np

def get_non_black_pixels(grid):
    # Find coordinates and colors of all non-black pixels
    coords = np.argwhere(grid != 0)
    colors = [grid[x, y] for x, y in coords]
    return list(zip(coords, colors))

def extend_line(grid, start_x, start_y, color):
    # Extend line horizontally, vertically, and including same-color diagonals
    height, width = grid.shape

    # Horizontal extension
    for y in range(width):
      if grid[start_x,y] == 0 or grid[start_x,y] == color:
        grid[start_x, y] = color

    # Vertical extension
    for x in range(height):
      if grid[x, start_y] == 0 or grid[x, start_y] == color:
        grid[x, start_y] = color

    # check diagonals
    for x_offset, y_offset in [(-1,-1),(-1,1),(1,-1),(1,1)]:
      x,y = start_x + x_offset, start_y + y_offset
      while 0 <= x < height and 0 <= y < width:
        if grid[x,y] == color:
            grid[x,y] = color # set
        else:
            break # stop
        x,y = x + x_offset, y+y_offset


def transform(input_grid):
    # Initialize output grid with the same dimensions and all black pixels
    output_grid = np.zeros_like(input_grid)

    # Get non-black pixels and their colors
    pixels = get_non_black_pixels(input_grid)


    # Create lines for each non-black pixel
    for (x, y), color in pixels:
        extend_line(output_grid, x, y, color)


    return output_grid
```
