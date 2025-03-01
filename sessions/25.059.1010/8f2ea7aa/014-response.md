# 8f2ea7aa • 014 • refine_coder

---
```python
"""
The transformation rule involves extending each contiguous horizontal region of orange pixels by one pixel on both the left and right sides.
"""

import numpy as np

def find_orange_regions(grid):
    """
    Finds all contiguous horizontal regions of orange pixels.
    Returns a list of lists, where each inner list contains the (row, col) coordinates of an orange region.
    """
    rows, cols = grid.shape
    orange_regions = []
    for r in range(rows):
        current_region = []
        for c in range(cols):
            if grid[r, c] == 7:
                current_region.append((r, c))
            else:
                if current_region:
                    orange_regions.append(current_region)
                    current_region = []
        if current_region:  # Handle regions that extend to the end of the row
            orange_regions.append(current_region)
    return orange_regions

def transform(input_grid):
    """
    Transforms the input grid by extending each contiguous horizontal orange region by one pixel on each side.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    orange_regions = find_orange_regions(input_grid)

    for region in orange_regions:
        # Extend left
        first_pixel_r, first_pixel_c = region[0]
        if first_pixel_c > 0:
            output_grid[first_pixel_r, first_pixel_c - 1] = 7

        # Extend Right
        last_pixel_r, last_pixel_c = region[-1]
        if last_pixel_c < cols - 1:
            output_grid[last_pixel_r, last_pixel_c + 1] = 7

    return output_grid
```
