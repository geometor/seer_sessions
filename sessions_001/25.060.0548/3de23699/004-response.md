# 3de23699 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Elements:** Locate the four yellow pixels (color 4) within the input grid. These act as corner markers, defining a conceptual square region within the larger input.
2.  **Ignore Other Elements:** Ignore everything else *except* the yellow pixels.
3.  **Define Bounding Box:** Create the smallest possible rectangular bounding box that encompasses the yellow pixels.
4.  **Crop and translate:** Crop the section described by bounding box.
5.  **Replace colors:** keep all color 4 intact. Change all other colors to 0.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def bounding_box(points):
    """Computes the bounding box of a set of points."""
    min_row = np.min(points[:, 0])
    max_row = np.max(points[:, 0])
    min_col = np.min(points[:, 1])
    max_col = np.max(points[:, 1])
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find yellow pixels (color 4).
    yellow_pixels = find_pixels_by_color(input_grid, 4)

    # Determine the bounding box.
    (min_row, min_col), (max_row, max_col) = bounding_box(yellow_pixels)
    
    # Initialize output grid based on bounding box size
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.zeros((height, width), dtype=int)

    # Crop and translate, while changing color
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if input_grid[r,c] == 4:
                output_grid[r-min_row, c-min_col] = 4


    return output_grid
```
