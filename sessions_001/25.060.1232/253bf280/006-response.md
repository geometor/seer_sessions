# 253bf280 • 006 • refine_coder

---
```python
"""
Identifies azure (8) pixels in the input grid and connects all azure pixels on the same row with a horizontal line of green (3) pixels, encompassing the entire range between the leftmost and rightmost azure pixels on each row.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def connect_all_pixels_on_row(grid, row, col_start, col_end, color):
    """Fills the space between two column indices on the same row with a given color."""
    grid[row, col_start:col_end+1] = color

def transform(input_grid):
    """Transforms the input grid by connecting all azure pixels on each row with green pixels."""
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find all azure pixels.
    azure_pixels = find_pixels_by_color(output_grid, 8)

    # Group azure pixels by row.
    pixels_by_row = {}
    for pixel in azure_pixels:
        row = pixel[0]
        if row not in pixels_by_row:
            pixels_by_row[row] = []
        pixels_by_row[row].append(pixel)

    # Connect all azure pixels on the same row.
    for row, pixels in pixels_by_row.items():
        # Ensure there are at least two pixels in the row to connect.
        if len(pixels) >= 2:
            # Find the minimum and maximum column indices.
            columns = [pixel[1] for pixel in pixels]
            min_col = min(columns)
            max_col = max(columns)
            connect_all_pixels_on_row(output_grid, row, min_col, max_col, 3)

    return output_grid
```
