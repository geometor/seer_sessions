# 4093f84a • 008 • refine_coder

---
```python
"""
1.  **Check for All-Gray Row:** Examine the input grid to determine if there's a row where all pixels are gray (color value 5).

2.  **Case 1: All-Gray Row Exists:**
    *   If an all-gray row exists, create a new grid with a height of 3 and the same width as the input grid.
    *   Copy the all-gray row and the row immediately above and below it from the input grid to the new output grid.
    * All copied rows should remain gray.

3.  **Case 2: No All-Gray Row:**
    *   If no all-gray row exists, create a new grid that has same width as the input grid, and the input grid's height minus 2 (remove top and bottom row).
    *   Fill all cells in the new grid with gray (color value 5).
"""

import numpy as np

def find_gray_row(grid):
    """Finds the index of the first all-gray row in a grid."""
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    gray_row_index = find_gray_row(input_grid)
    input_grid_height = input_grid.shape[0]
    input_grid_width = input_grid.shape[1]

    if gray_row_index != -1:
        # Case 1: All-Gray Row Exists
        output_grid = np.full((3, input_grid_width), 5, dtype=int)
        start_row = max(0, gray_row_index - 1)
        end_row = min(input_grid_height, gray_row_index + 2)

        # Adjust for boundary conditions
        if(gray_row_index == 0):
            output_grid[1,:] = input_grid[gray_row_index,:]
            output_grid[2,:] = input_grid[gray_row_index+1,:]
        elif(gray_row_index == input_grid_height-1):
            output_grid[0,:] = input_grid[gray_row_index-1,:]
            output_grid[1,:] = input_grid[gray_row_index,:]
        else: # Copy rows, ensure all gray
            output_grid[0, :] = input_grid[gray_row_index - 1, :]
            output_grid[1,:] = input_grid[gray_row_index,:]
            output_grid[2, :] = input_grid[gray_row_index + 1, :]

        return output_grid

    else:
        # Case 2: No All-Gray Row
        output_grid = np.full((input_grid_height - 2, input_grid_width), 5, dtype=int)
        return output_grid
```
