# 54d82841 • 012 • refine_coder

---
```python
"""
1. Find Green: Locate all green pixels (value 3) in the input grid.
2. Identify Bottom-Most Row: Find the row with the largest row index that contains at least one green pixel.
3. Find Target Pixel Column: Consider white pixels in rows below the row
   found in the previous step. The target is a white pixel below this row.
4. Transform: Change the target pixel's color from white (0) to yellow (4).
"""

import numpy as np

def find_green_pixels(grid):
    # Find coordinates of all green pixels.
    green_coords = np.argwhere(grid == 3)
    return green_coords

def find_bottom_most_row(green_coords):
    # Find the bottom-most row containing green pixels.
    if len(green_coords) == 0:
        return -1  # No green pixels, so no bottom-most row
    max_row = np.max(green_coords[:, 0])
    return max_row

def find_target_pixel(grid, bottom_most_row):
    # Find the target white pixel (0) below the bottom-most green row.
    rows, cols = grid.shape
    
    if bottom_most_row == -1 or bottom_most_row == rows -1:
       return None

    target_row = -1
    target_col = -1

    for row in range(bottom_most_row + 1, rows):
        for col in range(cols):
            if grid[row, col] == 0:
                if target_row == -1:
                    target_row = row
                    target_col = col
                elif col < target_col:
                    target_row = row
                    target_col = col

    if target_row != -1:
       return (target_row, target_col)
    else:
        return None
    

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)

    # Find green pixels.
    green_pixels = find_green_pixels(output_grid)

    # Find the bottom-most row with green pixels.
    bottom_most_row = find_bottom_most_row(green_pixels)

    # Find the target white pixel.
    target_pixel = find_target_pixel(output_grid, bottom_most_row)
   
    # Change the target pixel to yellow if found.
    if target_pixel:
        output_grid[target_pixel[0], target_pixel[1]] = 4

    return output_grid
```
