# 8731374e • 018 • refine_coder

---
```python
"""
Extract a cross-shaped subgrid from a larger input grid. The cross is formed by red (2) pixels, and the background is azure (8).
"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross pattern
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 2:
              if is_cross_center(grid, r, c):
                return (r, c)
    return None

def is_cross_center(grid, r, c):
    # check cross pattern existence with current center
    rows, cols = grid.shape
    
    # Check horizontal
    if not (0< c < cols -1 and grid[r,c-1] == 2 and grid[r, c+1] == 2):
        return False
        
    # Check vertical
    if not (0 < r < rows - 1 and grid[r-1,c] == 2 and grid[r+1, c] == 2):
        return False    
    
    return True

def get_cross_dimensions(grid, center_row, center_col):
    # get full dimensions of the cross

    rows, cols = grid.shape
    
    # Horizontal
    left = center_col
    while left >= 0 and grid[center_row, left] == 2:
        left -= 1
    right = center_col
    while right < cols and grid[center_row, right] == 2:
        right += 1
        
    # Vertical
    up = center_row
    while up >= 0 and grid[up, center_col] == 2:
        up -= 1
    down = center_row
    while down < rows and grid[down, center_col] == 2:
        down += 1

    return (up, down, left, right)

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find the center of the cross
    center = find_cross_center(grid)
    if center is None:
        return [[]] # Return empty grid if no cross is found

    center_row, center_col = center

    # Get cross boundaries
    up, down, left, right = get_cross_dimensions(grid, center_row, center_col)

    # Determine output grid size, adding the surrounding 8s
    out_up = up -1
    out_down = down + 1
    out_left = left - 1
    out_right = right + 1
    
    
    # boundary checks
    out_up = max(0, out_up)
    out_left = max(0, out_left)
    out_down = min(grid.shape[0], out_down)
    out_right = min(grid.shape[1], out_right)
   
    # Ensure at least 2 azure pixels on the left if possible
    if out_left > 0:
      out_left -=1

    # Extract subgrid
    output_grid = grid[out_up:out_down, out_left:out_right]

    return output_grid.tolist()
```
