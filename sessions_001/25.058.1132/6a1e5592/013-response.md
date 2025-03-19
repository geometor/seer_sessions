# 6a1e5592 • 013 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all red pixels within the input grid.
2.  **Define Transformed Region:** Create a rectangular region. The top of the region is defined by the highest row containing a red pixel, and the bottom of the region is the row containing the lowest red pixel. The left side of the region is the column of the left-most red pixel and the right side is the column of the right-most red pixel.
3. **Remove Gray Pixels:** Change all gray pixels outside of the transformed region to white.
4.  **Transform White Pixels:** Within the transformed region, change white pixels to blue pixels if those white pixels appear to the right of the right-most red pixel in the same row.
5.  **Preserve Red Pixels:** Red pixels remain unchanged.
"""

import numpy as np

def get_red_positions(grid):
    return np.array(np.where(grid == 2)).T

def get_transformed_region_bounds(grid):
    red_positions = get_red_positions(grid)
    if len(red_positions) == 0:
        return None  # No red pixels

    min_row = np.min(red_positions[:, 0])
    max_row = np.max(red_positions[:, 0])
    min_col = np.min(red_positions[:, 1])
    max_col = np.max(red_positions[:, 1])

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define Transformed Region
    bounds = get_transformed_region_bounds(input_grid)
    if bounds is None:
        return output_grid
    min_row, max_row, min_col, max_col = bounds

    # Remove Gray Pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 0

    # Transform White Pixels within the region
    for r in range(min_row, max_row + 1):
        for c in range(min_col, cols):
          if input_grid[r,c] == 0 and c > max_col:
            output_grid[r,c] = 1

    return output_grid
```
