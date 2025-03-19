# 3-1e0a9b12 • 012 • refine_coder

---
```python
"""
1.  **Identify Anchors:** The yellow ('4') and orange ('7') pixels form a vertically adjacent anchor group. These pixels do not change position.

2.  **Identify Movers:** The azure ('8') and maroon ('9') pixels are potential movers.

3.  **Move '8':** Move the azure ('8') pixel down as far as possible within its *original column*. It stops when it reaches the bottom edge of the grid or another non-white pixel.

4.  **Move '9' (Conditionally):**
    *   Check if '9' is initially to the *right* of '8' (i.e., '9''s initial column index is greater than '8''s initial column index).
    *   If '9' is to the right of '8', move '9' to the cell immediately to the right of the *new* position of '8'.
    *   If '9' is *not* to the right of '8', '9' does *not* move.

5.  **Preserve Background:** All other white ('0') pixels remain unchanged.
"""

import numpy as np

def find_object(grid, value):
    # Find the coordinates of a specific value in the grid.
    coords = np.argwhere(grid == value)
    return coords[0] if coords.size > 0 else None

def move_element_down_in_column(grid, start_coords):
    # Move an element down as far as possible within its column.
    row, col = start_coords
    while row + 1 < grid.shape[0] and grid[row + 1, col] == 0:
        row += 1
    return row, col

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find anchor elements (4 and 7) - not used in logic, but good practice.
    coords_4 = find_object(output_grid, 4)
    coords_7 = find_object(output_grid, 7)

    # Find mover elements (8 and 9).
    coords_8 = find_object(output_grid, 8)
    coords_9 = find_object(output_grid, 9)
    
    if coords_8 is not None:
        # Move '8' down in its column.
        new_coords_8 = move_element_down_in_column(output_grid, coords_8)

        # Clear original position of '8'.
        output_grid[coords_8[0], coords_8[1]] = 0
        # Set new position of '8'.
        output_grid[new_coords_8[0], new_coords_8[1]] = 8
    else:
        new_coords_8 = None  # Handle case where '8' doesn't exist


    if coords_9 is not None and new_coords_8 is not None:
        # Check if '9' is to the right of '8' initially.
        if coords_9[1] > coords_8[1]:
            # Move '9' to the right of new '8' position.
            output_grid[coords_9[0], coords_9[1]] = 0
            output_grid[new_coords_8[0], new_coords_8[1] + 1] = 9

    return output_grid
```

