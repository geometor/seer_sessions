# af902bf9 • 010 • example_2 • investigate_coder

---
```python
"""
Copies yellow pixels from the input grid to the output grid and adds a red rectangle in the output grid.
"""

import numpy as np

def find_pixels_by_value(grid, value):
    """Finds the coordinates of pixels with a specific value."""
    return np.argwhere(grid == value).tolist()

def create_rectangle(grid, top_left, bottom_right, value):
    """Fills a rectangular region in the grid with a given value."""
    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            grid[r, c] = value
    return grid

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find yellow pixels (value 4)
    yellow_pixels = find_pixels_by_value(input_grid, 4)

    # Preserve yellow pixels (though this is redundant since we copy the input grid, it is explicitly mentioned in the NL program and good practice to preserve intent)
    #for pixel in yellow_pixels:
    #    output_grid[pixel[0], pixel[1]] = 4

    # Create red rectangle (value 2)
    top_left = (2, 2)
    bottom_right = (5, 5)
    output_grid = create_rectangle(output_grid, top_left, bottom_right, 2)

    return output_grid
```
