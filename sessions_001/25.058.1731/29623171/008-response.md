# 29623171 • 008 • refine_coder

---
```python
"""
Preserve all gray lines. Remove blue pixels that are not connected to any gray
pixel (directly or indirectly). Create a 3x3 blue square at the bottom-right,
aligned with the rightmost edge of the bottom-most gray line, and the bottom
edge of the gray line.
"""

import numpy as np

def get_gray_lines(grid, gray_color=5):
    """Finds all gray lines and returns their pixels."""
    rows, cols = grid.shape
    gray_lines = []
    for r in range(rows):
        gray_pixels_in_row = []
        for c in range(cols):
            if grid[r, c] == gray_color:
                gray_pixels_in_row.append((r, c))
        if gray_pixels_in_row:  # Found a line
            gray_lines.append(gray_pixels_in_row)
    return gray_lines

def is_adjacent(pixel1, pixel2):
    """Checks if two pixels are adjacent (up, down, left, or right)."""
    r1, c1 = pixel1
    r2, c2 = pixel2
    return (abs(r1 - r2) == 1 and c1 == c2) or (r1 == r2 and abs(c1 - c2) == 1)

def get_connected_component(grid, start_pixel, color):
    """Gets the connected component of a given color starting from a pixel."""
    rows, cols = grid.shape
    queue = [start_pixel]
    visited = {start_pixel}
    component = [start_pixel]

    while queue:
        r, c = queue.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                grid[nr, nc] == color and (nr, nc) not in visited):
                queue.append((nr, nc))
                visited.add((nr, nc))
                component.append((nr, nc))
    return component


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Preserve Gray Lines (and find bottom-most for square placement)
    gray_lines = get_gray_lines(input_grid)
    bottom_gray_line = []
    if gray_lines:
        bottom_gray_line = gray_lines[-1] # for placement of the blue square

    # Identify and Remove Unconnected Blue Pixels
    all_gray_pixels = [pixel for line in gray_lines for pixel in line]
    connected_blue_pixels = set()
    for gray_pixel in all_gray_pixels:
        connected_blue_pixels.update(get_connected_component(input_grid, gray_pixel, 1))

    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 1 and (r,c) not in connected_blue_pixels:
                output_grid[r,c] = 0 # clear unconnected

    # Create 3x3 Blue Square (Conditional on gray line existing)
    if bottom_gray_line:
        rightmost_gray_pixel = bottom_gray_line[-1]  # Get right-most pixel
        bottom_row = rightmost_gray_pixel[0] # get the row
        start_col = rightmost_gray_pixel[1] - 2  # start col for blue square

        for r in range(bottom_row, min(bottom_row + 3, rows)):
            for c in range(max(0, start_col), min(start_col + 3, cols)):
                output_grid[r, c] = 1

    return output_grid
```
