# ff28f65a • 038 • refine_coder

---
```python
"""
Divide the input grid into nine regions, forming a 3x3 meta-grid.  For each region: If a region contains any red pixels (2), the corresponding cell in the output grid is blue (1). If there are no red pixels, and the region consists *only* of orange pixels (7), set the output cell to white (0). Regions with any other combination default to white (0) because of initialization.
"""

import numpy as np

def get_region_bounds(input_grid, row_index, col_index):
    """Calculates the row and column bounds for a region in the input grid."""
    rows, cols = input_grid.shape
    region_height = rows // 3
    region_width = cols // 3
    row_start = row_index * region_height
    row_end = row_start + region_height
    if row_index == 2:
        row_end = rows  # Ensure the last row region extends to the edge
    col_start = col_index * region_width
    col_end = col_start + region_width
    if col_index == 2:
        col_end = cols  # Ensure the last col region extends to the edge
    return row_start, row_end, col_start, col_end

def check_region_for_colors(input_grid, row_start, row_end, col_start, col_end):
    """Checks a region for the presence of red and only orange pixels."""
    contains_red = False
    contains_only_orange = True

    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if input_grid[r, c] == 2:
                contains_red = True
                contains_only_orange = False  # If red is found, it's not only orange
                break  # Optimization: Exit inner loop once red is found.
            elif input_grid[r, c] != 7:
                contains_only_orange = False
        if contains_red:
            break # Optimization: exit outer loop

    return contains_red, contains_only_orange

def transform(input_grid):
    """Transforms the input grid based on the presence of red and orange colors."""

    # Initialize the 3x3 output grid with all white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 meta-grid.
    for row_index in range(3):
        for col_index in range(3):
            # Get the bounds of the current region.
            row_start, row_end, col_start, col_end = get_region_bounds(input_grid, row_index, col_index)

            # Check the region for red and other colors.
            contains_red, contains_only_orange = check_region_for_colors(input_grid, row_start, row_end, col_start, col_end)

            # Determine the output pixel value.
            if contains_red:
                output_grid[row_index, col_index] = 1  # Red presence: Blue
            elif contains_only_orange:
                output_grid[row_index, col_index] = 0 # Only Orange: White (default)
            # else any other colors: defaults to white

    return output_grid
```
