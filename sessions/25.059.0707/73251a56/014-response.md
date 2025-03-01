# 73251a56 • 014 • refine_coder

---
```python
"""
The transformation rule identifies the single non-white pixel in the input grid. This pixel is then copied to the bottom-right corner of the 3x3 output grid. If the input has one and only one non-white pixel, place that pixel in the bottom right cell, otherwise fill the 3x3 output with 0.
"""

import numpy as np

def find_non_white_pixel(grid):
    """Finds the coordinates of the single non-white pixel in the grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A tuple (row, col) representing the coordinates of the non-white pixel,
        or None if there isn't exactly one non-white pixel.
    """
    non_white_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white_pixels.append((r, c))
    if len(non_white_pixels) == 1:
        return non_white_pixels[0]
    else:
        return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # find the non-white pixel
    non_white_pixel_coords = find_non_white_pixel(input_grid)

    # change output pixels if exactly one found
    if non_white_pixel_coords:
        row, col = non_white_pixel_coords
        output_grid[2, 2] = input_grid[row, col]  # Place at bottom-right (2,2)

    return output_grid
```

