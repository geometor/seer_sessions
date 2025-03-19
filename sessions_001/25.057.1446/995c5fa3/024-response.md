# 995c5fa3 • 024 • refine_coder

---
```python
"""
Transforms an input grid containing white (0) pixels on a gray (5) background into a 3x3 output grid. The output grid represents the presence and orientation of white pixels: red (2) for horizontal, yellow (4) for vertical, and white (0) if no white pixels are present.
"""

import numpy as np

def find_white_pixels(grid):
    """Finds the coordinates of all white pixels in the grid."""
    return np.argwhere(grid == 0)

def has_horizontal_line(white_pixels):
    """Checks if the white pixels form a horizontal line (at least two adjacent)."""
    if len(white_pixels) < 2:
        return False
    rows = white_pixels[:, 0]
    cols = white_pixels[:, 1]
    
    # Check for adjacent columns in same row
    for row in np.unique(rows):
        cols_in_row = sorted(cols[rows == row])
        for i in range(len(cols_in_row) - 1):
            if cols_in_row[i+1] - cols_in_row[i] == 1:
                return True
    return False


def has_vertical_line(white_pixels):
    """Checks if the white pixels form a vertical line (at least two adjacent)."""
    if len(white_pixels) < 2:
        return False
    rows = white_pixels[:, 0]
    cols = white_pixels[:, 1]
    
    # Check for adjacent rows with same col
    for col in np.unique(cols):
        rows_in_col = sorted(rows[cols == col])
        for i in range(len(rows_in_col) - 1):
            if rows_in_col[i+1] - rows_in_col[i] == 1:
                return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find white pixels
    white_pixels = find_white_pixels(input_grid)

    # If no white pixels, return all-white grid
    if len(white_pixels) == 0:
        return output_grid

    # Check for horizontal and vertical lines
    if has_horizontal_line(white_pixels):
        output_grid[1, 1] = 2  # Center for horizontal
    if has_vertical_line(white_pixels):
        output_grid[1, 1] = 4 # Center for vertical

    return output_grid
```
