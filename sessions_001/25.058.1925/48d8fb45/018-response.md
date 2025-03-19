# 48d8fb45 • 018 • refine_coder

---
```python
"""
1.  Identify Red Pixels: Locate all pixels with the color red (value 2) within the input grid.
2.  Determine Overall Bounding Box: Find the minimum bounding box that encompasses *all* red pixels found in the input grid.
3.  Extract Subgrid: Extract the subgrid defined by this overall bounding box.
4.  Output: The extracted subgrid is the output.
"""

import numpy as np

def find_red_pixels(grid):
    # Find coordinates of all red pixels
    red_pixels = []
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 2:
                red_pixels.append((row, col))
    return red_pixels

def get_overall_bounding_box(red_pixels):
    # Determine the bounding box of all red pixels
    if not red_pixels:
        return 0, 0, 0, 0  # Or some other default/error value
    min_row = min(pixel[0] for pixel in red_pixels)
    max_row = max(pixel[0] for pixel in red_pixels)
    min_col = min(pixel[1] for pixel in red_pixels)
    max_col = max(pixel[1] for pixel in red_pixels)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # 1. Identify Red Pixels
    red_pixels = find_red_pixels(input_grid)

    # 2. Determine Overall Bounding Box
    min_row, min_col, max_row, max_col = get_overall_bounding_box(red_pixels)

    # 3. Extract Subgrid
    if not red_pixels: #handle no red pixels
        output_grid = np.empty((0, 0), dtype=int)
    else:
        output_grid = input_grid[min_row:max_row + 1, min_col:max_col + 1]

    # 4. Output
    return output_grid
```
