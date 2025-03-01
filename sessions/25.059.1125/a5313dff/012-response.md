# a5313dff • 012 • refine_coder

---
```python
"""
The transformation rule identifies all closed shapes formed by red (2) pixels and fills their interior with blue (1) pixels. The red boundary pixels and the white (0) background remain unchanged.  If a red shape is not closed, it is not filled.
"""

import numpy as np

def get_object(grid, color):
    # returns a mask representing the object of given color
    obj = (grid == color)
    return obj.astype(int)

def flood_fill(grid, x, y, target_color, replacement_color):
    """
    Performs a flood fill operation on the grid, starting from the given coordinates.

    Args:
    grid: The input grid (as a numpy array).
    x: The starting x-coordinate.
    y: The starting y-coordinate.
    target_color: The color to be replaced.
    replacement_color: The new color.
    """
    if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1] or grid[x, y] != target_color:
        return

    grid[x, y] = replacement_color
    flood_fill(grid, x + 1, y, target_color, replacement_color)
    flood_fill(grid, x - 1, y, target_color, replacement_color)
    flood_fill(grid, x, y + 1, target_color, replacement_color)
    flood_fill(grid, x, y - 1, target_color, replacement_color)

def is_closed(grid, red_object):
    """
    Checks if a red object is closed.

    Args:
    grid: The original input grid.
    red_object: A mask representing the red object (1 for red pixels, 0 otherwise).
    """
    # Find the bounding box of the red object
    rows, cols = np.where(red_object)
    if len(rows) == 0:  # Handle empty object case
        return False
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    # Create a temporary grid slightly larger than the bounding box to detect boundary leaks.
    temp_grid = np.zeros((max_row - min_row + 3, max_col - min_col + 3), dtype=int)

    # Copy the red object into the temporary grid, offset by 1 in each dimension.
    for r, c in zip(rows, cols):
        temp_grid[r - min_row + 1, c - min_col + 1] = 1
        
    # Copy the values of the pixels inside the object
    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col+1):
        if grid[r,c] != 2:
            temp_grid[r - min_row+1, c- min_col +1] = -1

    # Perform flood fill from the edges of the temporary grid. Use a distinct value (e.g., 2).
    flood_fill(temp_grid, 0, 0, 0, 2)

    # If any red pixel (value 1) is adjacent to the flood-filled area (value 2),
    # the shape is not closed.
    for r in range(1, temp_grid.shape[0] - 1):
        for c in range(1, temp_grid.shape[1] - 1):
            if temp_grid[r, c] == 1:
                if (temp_grid[r + 1, c] == 2 or temp_grid[r - 1, c] == 2 or
                    temp_grid[r, c + 1] == 2 or temp_grid[r, c - 1] == 2):
                    return False
    
    # set interior pixels
    for r in range(1, temp_grid.shape[0] - 1):
      for c in range(1, temp_grid.shape[1] - 1):
        if temp_grid[r,c] == -1:
          temp_grid[r,c] = 3 # mark as interior
    return True

def fill_interior(grid, red_object):
  rows, cols = np.where(red_object)
  min_row, max_row = np.min(rows), np.max(rows)
  min_col, max_col = np.min(cols), np.max(cols)
  temp_grid = np.zeros((max_row - min_row + 3, max_col - min_col + 3), dtype=int)
  for r, c in zip(rows, cols):
      temp_grid[r - min_row + 1, c - min_col + 1] = 1

  # Copy the values of the pixels inside the object
  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col+1):
      if grid[r,c] != 2:
          temp_grid[r - min_row+1, c- min_col +1] = -1
  # flood_fill with 2
  flood_fill(temp_grid, 0, 0, 0, 2)

  for r in range(1, temp_grid.shape[0] - 1):
    for c in range(1, temp_grid.shape[1] - 1):
      if temp_grid[r,c] == -1:
        temp_grid[r,c] = 3 # mark as interior
  
  return temp_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # extract object defined by red pixels
    red_object = get_object(input_grid, 2)

    # Check if the red object is closed
    if is_closed(input_grid, red_object):
        # fill interior
        filled_grid = fill_interior(input_grid, red_object)
        rows, cols = np.where(red_object)
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        # set interior as blue (1)
        for i in range(filled_grid.shape[0]):
          for j in range(filled_grid.shape[1]):
            if filled_grid[i,j] == 3:
              output_grid[min_row+i-1, min_col+j-1] = 1

    return output_grid
```
