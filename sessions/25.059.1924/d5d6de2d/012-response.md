# d5d6de2d • 012 • refine_coder

---
```python
"""
Identifies a red shape in the input grid, removes it, and replaces it with one or two green pixels centered within the original shape's location. The number of green pixels depends on whether the shape is solid or not.
"""

import numpy as np

def find_red_shape(grid):
    rows, cols = grid.shape
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                red_pixels.append((r, c))
    return red_pixels

def is_solid_square(grid, red_pixels):
    if not red_pixels:
        return False

    min_row = min(r for r, c in red_pixels)
    max_row = max(r for r, c in red_pixels)
    min_col = min(c for r, c in red_pixels)
    max_col = max(c for r, c in red_pixels)

    if (max_row - min_row) != (max_col - min_col):
        return False

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r, c) not in red_pixels:
                return False  # Not solid
    return True

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Find the red shape
    red_pixels = find_red_shape(input_grid)
    
    if red_pixels:
        #find top-left and bottom-right pixels    
        min_row = min(r for r, c in red_pixels)
        max_row = max(r for r, c in red_pixels)
        min_col = min(c for r, c in red_pixels)
        max_col = max(c for r, c in red_pixels)

        # Calculate center of shape
        center_row = (min_row + max_row) // 2
        center_col = (min_col + max_col) // 2

        # Remove the red shape
        for r, c in red_pixels:
            output_grid[r, c] = 0

        # Add the green pixel(s)
        if is_solid_square(input_grid, red_pixels):
            output_grid[center_row, center_col] = 3
        else:
            output_grid[center_row, center_col] = 3
            output_grid[center_row + 1, center_col] = 3

    return output_grid
```
