# 47c1f68c • 008 • refine_coder

---
```python
"""
1. Remove Blue: Eliminate all blue pixels (value 1) from the input grid.
2. Identify Center: Determine the center row and column of the grid.
3. Detect Red Cross: Check for a red (value 2) cross shape centered in the grid. A cross is defined as a contiguous set of red pixels extending outwards from the center pixel, in all four cardinal directions (up, down, left, right), forming lines of equal length, and with length > 1.
4. Resize or Remove: if a red cross exists at the center, reduce it to a 5x5 cross centered at the original center, and remove all other red. If there is no red cross at the center, remove all red.
5. Return grid: return the modified grid
"""

import numpy as np

def find_object(grid, color):
    obj_coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color:
              obj_coords.append((r,c))
    return obj_coords

def is_cross_pixel(r, c, grid):
    # Check for at least one neighbor in both horizontal and vertical directions
    if grid[r,c] != 2:
      return False
    has_horizontal_neighbor = (c > 0 and grid[r, c-1] == 2) or (c < grid.shape[1]-1 and grid[r, c+1] == 2)
    has_vertical_neighbor = (r > 0 and grid[r-1, c] == 2) or (r < grid.shape[0]-1 and grid[r+1, c] == 2)
    return has_horizontal_neighbor and has_vertical_neighbor

def is_center_cross(grid):
    center_row, center_col = grid.shape[0] // 2, grid.shape[1] // 2
    return is_cross_pixel(center_row, center_col, grid)
  
def get_cross_size(grid):
    center_row, center_col = grid.shape[0] // 2, grid.shape[1] // 2
      #determine cross size:
      #find first row, starting at center
    first_row = center_row
    while first_row >= 0:
        if grid[first_row, center_col] == 2:
          first_row -= 1
        else:
          break
    first_row += 1
    last_row = center_row
    while last_row < grid.shape[0]:
        if grid[last_row, center_col] == 2:
            last_row += 1
        else:
            break
    cross_size = (last_row-first_row, last_row-first_row)
    return cross_size

def transform(input_grid):
    # initialize output_grid as copy of input, and set all to 0 (white)
    output_grid = np.copy(input_grid)
    output_grid[:] = 0

    # Remove blue pixels
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 1:
          output_grid[r,c] = 0

    # Find center row and column
    center_row = input_grid.shape[0] // 2
    center_col = input_grid.shape[1] // 2

    # Check for a red cross and construct 5x5 red cross
    if is_center_cross(input_grid):
      for r in range(center_row - 2, center_row + 3):
          for c in range(center_col - 2, center_col + 3):
              if 0 <= r < output_grid.shape[0] and 0<= c < output_grid.shape[1]:
                output_grid[r,c] = 2

    else: #remove all red pixels if no cross
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if output_grid[r,c] == 2:
                  output_grid[r,c] = 0

    return output_grid
```
