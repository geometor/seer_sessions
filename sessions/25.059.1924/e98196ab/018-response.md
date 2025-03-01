# e98196ab • 018 • refine_coder

---
```python
"""
1.  **First Row Transformation:** The first row of the output grid consists of red pixels (value 2) placed at the x-coordinates (column indices) where red pixels were present in the input grid.
2.  **Preserve Remaining Rows:** All rows from the input grid, except the first, are copied to the output grid, preserving their original order and content, *except* for the transformation described in step 3.
3.  **Last Row Red-to-Blue:** In the last row of the input grid, the rightmost red pixel (value 2) is changed to a blue pixel (value 1) in the corresponding position of the output grid.

"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array.
    output_grid = np.copy(input_grid)  # Start with a copy

    # 1. First Row Transformation:
    red_pixels = find_pixels_by_color(input_grid, 2)
    output_grid[0, :] = 0  # Clear the first row
    for coord in red_pixels:
        output_grid[0, coord[1]] = 2

    # 2. Preserve Remaining Rows (already done by copying)
    
    # 3. Last Row Red-to-Blue:
    red_pixels_last_row = []
    last_row_index = input_grid.shape[0] - 1
    for x, y in red_pixels:
      if x == last_row_index:
        red_pixels_last_row.append([x,y])
    
    if len(red_pixels_last_row) > 0:
      last_red_pixel = max(red_pixels_last_row, key=lambda item: item[1])
      output_grid[last_row_index, last_red_pixel[1]] = 1

    return output_grid.tolist()
```
