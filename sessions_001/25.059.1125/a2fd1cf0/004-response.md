# a2fd1cf0 • 004 • example_1 • investigate_coder

---
```python
"""
Identifies a red pixel (2) and a green pixel (3) in the input grid. Creates a path of azure pixels (8) connecting the red and green pixels. The path extends vertically from the red pixel to the row of the green pixel, then horizontally to connect the green pixel.
"""

import numpy as np

def find_pixel_by_color(grid, color_value):
    """Finds the coordinates of the first pixel with the specified color value."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color_value:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid by connecting a red and green pixel with an azure path."""
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the red and green pixels
    red_pos = find_pixel_by_color(input_grid, 2)
    green_pos = find_pixel_by_color(input_grid, 3)

    if red_pos is None or green_pos is None:
        return output_grid  # Return original grid if pixels are not found

    # Create the vertical path
    for row in range(red_pos[0] + 1, green_pos[0] + 1):
        output_grid[row, red_pos[1]] = 8

    # connect to green:
    output_grid[green_pos[0], green_pos[1]-1] = 8
    # change output pixels

    return output_grid
```
