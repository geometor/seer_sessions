# d5d6de2d • 014 • refine_coder

---
```python
"""
Identifies a red shape in the input grid, removes it, and replaces it with one or two green pixels centered within the original shape's location. The number of green pixels depends on whether the shape is solid or not.
"""

import numpy as np

def find_red_shape(grid):
    """Finds all red pixels in the grid."""
    rows, cols = grid.shape
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                red_pixels.append((r, c))
    return red_pixels

def is_solid(grid, pixels):
    """Checks if a shape defined by 'pixels' is solid."""
    if not pixels:
        return False

    # Find bounding box
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)

    # Check for any non-red pixels within the bounding box
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r, c) in pixels:
                if grid[r,c] != 2:
                    return False # internal pixel is wrong color
            elif grid[r,c] != 0:
                return False # region contains pixel of non-background inside bounding box, but not part of shape
    return True

def calculate_center(pixels):
    """Calculates the center of a shape defined by 'pixels'."""
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)

    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    return center_row, center_col

def transform(input_grid):
    # Create a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the red shape
    red_pixels = find_red_shape(input_grid)

    if red_pixels:
        # Calculate center of shape
        center_row, center_col = calculate_center(red_pixels)

        # Remove the red shape
        for r, c in red_pixels:
            output_grid[r, c] = 0

        # Add the green pixel(s)
        if is_solid(input_grid, red_pixels):
            output_grid[center_row, center_col] = 3  # One green pixel for solid shapes
        else:
            output_grid[center_row, center_col] = 3  # Two green pixels for hollow shapes
            output_grid[center_row + 1, center_col] = 3

    return output_grid
```
