# 2013d3e2 • 010 • refine_coder

---
```python
"""
1. Identify the inner core: Locate the smallest possible rectangle, 1x1 in size (a single pixel), of a non-blue color, that is inside a blue square of 3x3.
2. Bounding Box: Identify a blue 3x3 square bounding box surrounding this core.
3. Extract: extract the identified blue square with the inner non-blue core.
"""

import numpy as np

def find_inner_core(grid):
    # Find non-blue pixels
    rows, cols = np.where(grid != 1)
    if len(rows) == 0:
        return None  # No non-blue pixel found

    # Check if any non-blue pixel is surrounded by blue pixels
    for row, col in zip(rows, cols):
      if is_surrounded_by_blue(grid, row, col):
        return (row,col)
    return None

def is_surrounded_by_blue(grid, row, col):
    # Define the 3x3 neighborhood around the pixel
    min_row, max_row = max(0, row - 1), min(grid.shape[0], row + 2)
    min_col, max_col = max(0, col - 1), min(grid.shape[1], col + 2)
    
    # Check if the neighborhood forms 3x3 blue square
    if (max_row - min_row) != 3 or (max_col - min_col) != 3:
        return False

    for r in range(min_row, max_row):
        for c in range(min_col, max_col):
            if (r,c) != (row,col): #skip the center
               if grid[r, c] != 1:  # Check if the surrounding pixels are blue
                 return False  # Not surrounded by blue
    return True

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Find the coordinates of the inner core pixel
    core_coords = find_inner_core(input_array)
    
    if core_coords is None:
      return input_grid #no transformation

    row, col = core_coords
        
    # Calculate bounding box (3x3)
    min_row, max_row = row - 1, row + 2
    min_col, max_col = col - 1, col + 2

    # Extract the 3x3 region
    output_grid = input_array[min_row:max_row, min_col:max_col].tolist()
    return output_grid
```
