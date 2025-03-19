# 3906de3d • 012 • refine_coder

---
```python
"""
Identifies a blue shape boundary and red pixels in the input grid. Fills the area upwards from the red pixels with red color, constrained by the blue boundary or the top edge of the grid.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def fill_upwards(grid, start_coords, boundary_color):
    """Fills the grid upwards from given start coordinates with red (2) until a boundary color or top edge is reached."""
    output_grid = np.copy(grid)
    for row, col in start_coords:
        current_row = row
        while current_row >= 0 and output_grid[current_row, col] != boundary_color:
            output_grid[current_row, col] = 2
            current_row -= 1
    return output_grid

def transform(input_grid):
    """Transforms the input grid by filling upwards from red pixels, bounded by blue."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find blue and red pixels
    blue_pixels = find_pixels(input_grid, 1)
    red_pixels = find_pixels(input_grid, 2)

    # Fill upwards from red pixels, bounded by blue
    output_grid = fill_upwards(output_grid, red_pixels, 1)

    return output_grid
```
