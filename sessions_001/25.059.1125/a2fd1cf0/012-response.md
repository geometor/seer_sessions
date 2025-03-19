# a2fd1cf0 • 012 • refine_coder

---
```python
"""
1.  **Locate:** Find the red (2) pixel and the green (3) pixel within the input grid.
2.  **Horizontal Segment:** Starting at the red pixel's location, draw a horizontal line of azure (8) pixels extending in the direction of the green pixel.  The horizontal line stops in the column before (or after, if the green is to the left) the green pixel.
3.  **Vertical Segment:** From the last azure pixel of the horizontal segment, draw a vertical line of azure (8) pixels extending in the direction of the green pixel. The line stops in the same row as the green pixel.
4. The red and green pixels must remain with their original color values.
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
    input_grid_array = np.array(input_grid)

    # 1. Locate red and green pixels
    red_loc = find_pixel(input_grid_array, 2)
    green_loc = find_pixel(input_grid_array, 3)

    if red_loc is None or green_loc is None:
        return output_grid  # Return original if either pixel is missing

    # 2. Horizontal Segment
    if red_loc[1] < green_loc[1]:  # Green is to the right of red
        for c in range(red_loc[1], green_loc[1]):
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] -1
    else:  # Green is to the left of red
        for c in range(green_loc[1] + 1, red_loc[1] + 1):
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] + 1

    # 3. Vertical Segment
    if red_loc[0] < green_loc[0]: #green is below red
      for r in range(red_loc[0], green_loc[0]):
        output_grid[r, last_horizontal_x] = 8
    else: #green is above red
      for r in range(green_loc[0], red_loc[0]):
          output_grid[r, last_horizontal_x] = 8


    return output_grid
```
