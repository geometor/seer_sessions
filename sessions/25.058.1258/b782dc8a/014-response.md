# b782dc8a • 014 • refine_coder

---
```python
"""
1.  **Identify the Axis:**
    *   Identify the contiguous regions of blue(1) and yellow(4)

2.  **Horizontal Mirroring:**
    *   Find the minimum and maximum column of the yellow pixels
    *   Within the identified region, and to the left of the minimum and to the right of the maximum, mirror the colors.
    *   For pixels to the left of the minimum yellow column: find the `mirror_c` by calculating `mirror_c =  min_yellow_col + (min_yellow_col - c) - 1`. If an azure, blue, or yellow pixel with the coordinate(`r`,`mirror_c`) is within the defined region, replace the color of pixel (`r`,`c`) with the mirrored color.
    *   For pixels to the right of the maximum yellow column: find the `mirror_c` by calculating `mirror_c =  max_yellow_col - (c - max_yellow_col) + 1`. If an azure, blue, or yellow pixel with the coordinate(`r`,`mirror_c`) is within the defined region, replace the color of pixel (`r`,`c`) with the mirrored color.

3.  **Vertical Mirroring:**
   * Find the minimum and maximum row of the blue pixels
   * Within the identified region, and above the minimum and below the maximum, mirror the colors.
   * For pixels above the minimum blue row, find the `mirror_r` by calculating `mirror_r = min_blue_row + (min_blue_row - r) - 1`. If an azure, blue, or yellow pixel with coordinate (`mirror_r`,`c`) is in a region, replace the color of pixel (`r`,`c`) with the mirrored color.
   * For pixels below the maximum blue row, find the `mirror_r` by calculating `mirror_r = max_blue_row - (r - max_blue_row) + 1`. If an azure, blue, or yellow pixel with coordinate (`mirror_r`,`c`) is in a region, replace the color of pixel (`r`,`c`) with the mirrored color.

4.  **Color Preservation:** Any pixels not within the mirrored region, or not of color azure, blue, or yellow within the mirrored region, retain their original color from the input grid.
"""

import numpy as np

def get_object_pixels(grid, color):
    """Finds the contiguous region of pixels of a given color."""
    rows, cols = grid.shape
    pixels = []
    for r in range(rows):
        for c in range(cols):
          if grid[r,c] == color:
            pixels.append((r,c))
    return pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Axis and Regions
    yellow_pixels = get_object_pixels(input_grid, 4)
    blue_pixels = get_object_pixels(input_grid, 1)

    if not yellow_pixels or not blue_pixels:
        return output_grid

    #Horizontal
    min_yellow_col = min(c for r, c in yellow_pixels)
    max_yellow_col = max(c for r, c in yellow_pixels)

    #Vertical
    min_blue_row = min(r for r, c in blue_pixels)
    max_blue_row = max(r for r, c in blue_pixels)

    # 2. Horizontal Mirroring
    for r in range(rows):
        for c in range(cols):
            # Left of min_yellow_col
            if c < min_yellow_col:
                mirror_c = min_yellow_col + (min_yellow_col - c) - 1
                if mirror_c < cols and input_grid[r, mirror_c] in [1, 4, 8]:
                    output_grid[r, c] = input_grid[r, mirror_c]
            # Right of max_yellow_col
            elif c > max_yellow_col:
                mirror_c = max_yellow_col - (c - max_yellow_col) + 1
                if mirror_c >= 0 and input_grid[r, mirror_c] in [1, 4, 8]:
                    output_grid[r, c] = input_grid[r, mirror_c]

    # 3. Vertical Mirroring
    for r in range(rows):
        for c in range(cols):
            # Above min_blue_row
            if r < min_blue_row:
                mirror_r = min_blue_row + (min_blue_row - r) - 1
                if mirror_r < rows and input_grid[mirror_r, c] in [1, 4, 8]:
                  output_grid[r,c] = input_grid[mirror_r,c]
            # Below max_blue_row
            elif r > max_blue_row:
                mirror_r = max_blue_row - (r - max_blue_row) + 1
                if mirror_r >=0 and input_grid[mirror_r, c] in [1, 4, 8]:
                    output_grid[r,c] = input_grid[mirror_r, c]

    return output_grid
```
