# 3befdf3e • 012 • refine_coder

---
```python
"""
1.  **Identify** the largest red square (color 2) in the input grid.
2.  **Identify** the single orange pixel (color 7) within the red square.
3.  **Expand** the red square. Add a single layer of red pixels around the perimeter of the original red square.
4.  **Modify** the orange pixel. The single orange turns into a sequence of orange, red, orange, in a horizontal line.
5. **Combine**: The expanded red square and the modified orange sequence form a single combined object, maintaining relative positions.
6.  **Place** the resulting combined shape in the output grid, replacing the corresponding pixels in the input grid. The top-left of the combined object in output is determined by the top-left of the original red square. The position of the modified orange pixels relative to the red square is maintained.
7. The background is unchanged.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Handle cases with no object of given color
    # Calculate the bounding box
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    return min_row, max_row, min_col, max_col

def expand_red_square(grid, min_row, max_row, min_col, max_col):
     # expand one unit each direction
    expanded_grid = grid.copy()

    new_min_row = max(0, min_row - 1)
    new_max_row = min(grid.shape[0] -1, max_row + 1)
    new_min_col = max(0, min_col - 1)
    new_max_col = min(grid.shape[1] - 1, max_col + 1)

    for r in range(new_min_row, new_max_row + 1):
      for c in range(new_min_col, new_max_col + 1):
                expanded_grid[r,c] = 2

    return expanded_grid, new_min_row, new_max_row, new_min_col, new_max_col

def modify_orange_pixel(grid, row, col):
    # modify the orange pixel to horizontal [7,2,7]
    modified_grid = grid.copy()

    modified_grid[row, col -1] = 7
    modified_grid[row, col] = 2
    modified_grid[row, col + 1] = 7

    return modified_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find the red square
    red_min_row, red_max_row, red_min_col, red_max_col = find_object(input_grid, 2)

    if red_min_row is None:
        return output_grid

    # expand red
    output_grid, red_min_row_new, red_max_row_new, red_min_col_new, red_max_col_new = expand_red_square(input_grid, red_min_row, red_max_row, red_min_col, red_max_col)

    # Find the orange square
    orange_min_row, orange_max_row, orange_min_col, orange_max_col = find_object(input_grid, 7)

    if orange_min_row is None:
      return output_grid

    # modify orange object, relative to original position
    output_grid = modify_orange_pixel(output_grid, orange_min_row , orange_min_col)

    return output_grid
```
