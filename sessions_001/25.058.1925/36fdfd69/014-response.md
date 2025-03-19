# 36fdfd69 • 014 • refine_coder

---
```python
"""
1.  **Identify Red Regions:** Locate all contiguous regions of red (2) pixels in the input grid. A "contiguous region" is a group of red pixels connected horizontally or vertically (not diagonally).

2.  **Identify Edge Pixels:** Within each red region, identify the "edge" pixels. An edge pixel is a red pixel that has at least one non-red neighbor (up, down, left, or right).

3.  **Transform Edge Pixels:** Change all identified edge pixels from red (2) to yellow (4).

4.  **Interior Pixels Unchanged:** Red pixels that are *not* edge pixels (i.e., they are completely surrounded by other red pixels) remain unchanged.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the values of adjacent pixels (up, down, left, right) for a given cell.
    """
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row-1, col])  # Up
    if row < rows - 1:
        adjacent.append(grid[row+1, col])  # Down
    if col > 0:
        adjacent.append(grid[row, col-1])  # Left
    if col < cols - 1:
        adjacent.append(grid[row, col+1])  # Right
    return adjacent

def is_edge_pixel(grid, row, col):
    """
    Checks if a red pixel is an edge pixel (has at least one non-red neighbor).
    """
    if grid[row, col] != 2:
        return False  # Only check red pixels

    adjacent_values = get_adjacent_pixels(grid, row, col)
    return any(val != 2 for val in adjacent_values)

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Red pixels on the edge of a contiguous red region become yellow.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is a red edge pixel
            if is_edge_pixel(input_grid, row, col):
                output_grid[row, col] = 4  # Change to yellow

    return output_grid
```

