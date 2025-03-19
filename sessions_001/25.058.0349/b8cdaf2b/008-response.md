# b8cdaf2b • 008 • example_2 • investigate_coder

---
```python
"""
Find the Green pixel, then make a vertical line of green pixels 
from the original up to the top. All of the other colors remain.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return coords[0]  # Return the first occurrence
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the green pixel (color 3)
    green_pixel_coord = find_pixel_by_color(input_grid, 3)

    if green_pixel_coord is not None:
        # Get the column index of the green pixel
        green_col = green_pixel_coord[1]

        # Iterate through rows above the green pixel, changing them to green
        for row in range(green_pixel_coord[0] -1, -1, -1):
            output_grid[row, green_col] = 3

    return output_grid
```
