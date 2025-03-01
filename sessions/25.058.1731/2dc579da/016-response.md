# 2dc579da • 016 • example_3 • investigate_coder

---
```python
"""
Find the azure (8) pixel. Crop a 5x5 square centered on it, excluding any
pixels that were a part of the blue cross in the original image.
"""

import numpy as np

def find_pixel_location(grid, color):
    # Find the location of a pixel with a specific color.
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return [r, c]
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find the location of the azure pixel (color 8).
    azure_location = find_pixel_location(input_grid, 8)

    # Determine the boundaries of the 5x5 crop centered on the azure pixel.
    row_start = azure_location[0] - 2
    row_end = azure_location[0] + 3
    col_start = azure_location[1] - 2
    col_end = azure_location[1] + 3

    # Extract the 5x5 subgrid.
    output_grid = input_grid[row_start:row_end, col_start:col_end]
    
    return output_grid.tolist()
```
