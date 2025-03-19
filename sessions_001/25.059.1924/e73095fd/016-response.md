# e73095fd • 016 • refine_coder

---
```python
"""
1.  **Identify the Gray Shape:** Locate the contiguous region of gray (5) pixels in the input grid. This forms the "gray_shape" object.
2.  **Determine Replacement Region:** Within the gray shape, a 3x3 rectangular block of gray pixels will always be replaced by yellow pixels.
3.  **Perform Replacement:** Change the color of the pixels in the determined 3x3 region from gray (5) to yellow (4).
"""

import numpy as np

def find_gray_shape(grid):
    # Find all gray pixels (value 5)
    gray_pixels = np.argwhere(grid == 5)
    return gray_pixels

def get_gray_shape_bounds(gray_pixels):
    # Get the bounding box of the gray shape
    if len(gray_pixels) == 0:
        return None
    min_row = np.min(gray_pixels[:, 0])
    max_row = np.max(gray_pixels[:, 0])
    min_col = np.min(gray_pixels[:, 1])
    max_col = np.max(gray_pixels[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find gray shape pixels
    gray_pixels = find_gray_shape(input_grid)

    # Get gray shape bounds
    bounds = get_gray_shape_bounds(gray_pixels)
    if bounds is None:
        return output_grid  # No gray shape found
    min_row, max_row, min_col, max_col = bounds

    # Determine the 3x3 replacement region. Start from top-left of gray area.
    replace_row_start = min_row + 1 # second row
    replace_col_start = min_col + 1 # second col
    if (max_row - min_row + 1) < 3:
      replace_row_start = min_row
    if (max_col-min_col + 1) < 3:
      replace_col_start = min_col

    for i in range(3):
        for j in range(3):
            if replace_row_start + i <= max_row and replace_col_start + j <= max_col:
                if output_grid[replace_row_start + i, replace_col_start + j] == 5: # added condition
                   output_grid[replace_row_start + i, replace_col_start + j] = 4


    return output_grid
```
