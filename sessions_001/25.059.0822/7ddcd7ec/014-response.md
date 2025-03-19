# 7ddcd7ec • 014 • refine_coder

---
```python
"""
1.  **Identify the Object:** Find the contiguous block of yellow (color 4) pixels in the input grid. This constitutes the "object".
2.  **Determine Target Row:** Identify the highest row index that contains only black(0) in the entire grid. This will be referred to as an "empty row". The row directly above the topmost "empty" row will be the "target row".
3. **Object Bottom Row:** find the object lowest row, the row with the highest index number.
4.  **Calculate Vertical Shift:** Calculate the difference between the "target row" and the row below the "Object Bottom Row". This is the "vertical shift".
5.  **Move the Object:** move the object down by the "vertical shift", such that its most bottom pixels touch the target row.
6. **Clear the Old Object:** make the locations where the original object was all black (0).
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

def calculate_vertical_shift(grid, object_bottom_row):
    # Calculate the vertical shift to move the object.
    rows = grid.shape[0]
    
    # Find the first empty row from the bottom
    empty_row_start = rows
    
    # iterate backward until content found
    for r in range(rows-1,-1, -1):
        if not all(x == 0 for x in grid[r]):
          break;
        empty_row_start = r

    target_row = empty_row_start -1
    return target_row - (object_bottom_row)

def transform(input_grid):
    # Initialize output_grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Find the yellow object and its boundaries.
    yellow_coords, top_left, bottom_right = find_object(input_grid, 4)
    
    if len(yellow_coords) == 0:
        return output_grid

    object_bottom_row = bottom_right[0]

    # calculate vertical shift
    vertical_shift = calculate_vertical_shift(output_grid, object_bottom_row)

    # Move the object.
    output_grid = move_object(output_grid, yellow_coords, vertical_shift)

    return output_grid
```
