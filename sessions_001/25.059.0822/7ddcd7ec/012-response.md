# 7ddcd7ec • 012 • refine_coder

---
```python
"""
Identify the yellow (4) object in the input grid. Move the object downwards, 
such that the bottom of the object aligns with the row immediately above 
the start of the empty rows at the bottom of the grid. The original object 
disappears.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return [], None, None
    # Find top-left and bottom-right corners
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return coords, (min_row, min_col), (max_row, max_col)

def move_object(grid, coords, row_shift):
    # Move the object down by row_shift.
    new_grid = np.copy(grid)
    
    # remove original
    for r, c in coords:
        new_grid[r, c] = 0

    # place in new location
    for r, c in coords:
        new_grid[r + row_shift, c] = 4
        
    return new_grid

def calculate_vertical_shift(grid, object_top_row, object_bottom_row):
    # Calculate the vertical shift to move the object.
    rows = grid.shape[0]
    
    # Find the first empty row from the bottom
    empty_row_start = rows
    
    # iterate backward until content found
    for r in range(rows-1,-1, -1):
        if not all(x == 0 for x in grid[r]):
          break;
        empty_row_start = r

    return empty_row_start - (object_bottom_row + 1)

def transform(input_grid):
    # Initialize output_grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Find the yellow object and its boundaries.
    yellow_coords, top_left, bottom_right = find_object(input_grid, 4)
    
    if not yellow_coords:
        return output_grid

    object_top_row = top_left[0]
    object_bottom_row = bottom_right[0]

    # calculate vertical shift
    vertical_shift = calculate_vertical_shift(output_grid, object_top_row, object_bottom_row)

    # Move the object.
    output_grid = move_object(output_grid, yellow_coords, vertical_shift)

    return output_grid
```
