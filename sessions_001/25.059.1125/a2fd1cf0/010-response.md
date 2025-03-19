# a2fd1cf0 • 010 • example_2 • investigate_coder

---
```python
"""
1. Locate the green (3) pixel in the input grid and copy it to the same location in the output grid.
2. Locate the red (2) pixel in the input grid.
3. In the output grid, at the same position of red pixel, create horizontal a line of azure (8) pixels extending to the right. The horizontal line ends in the column before the green pixel.
4. Create a vertical line of azure (8) pixel, starting from the position of the last azure pixel of the horizontal line. This line extends vertically upwards until the row above the green pixel.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the location of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)

    # 1. Copy the green pixel
    green_loc = find_pixel(input_grid, 3)
    if green_loc:  # Check if green_loc is not None
      output_grid[green_loc] = 3

    # 2. Locate the red pixel
    red_loc = find_pixel(input_grid, 2)

    # 3. & 4. Expand to azure line and connect
    if red_loc and green_loc :
        #horizontal line
        for c in range(red_loc[1], green_loc[1]):
            output_grid[red_loc[0], c] = 8
        #vertical line
        for r in range(red_loc[0]-1, green_loc[0]-1, -1):
            output_grid[r,green_loc[1]-1] = 8



    return output_grid
```
