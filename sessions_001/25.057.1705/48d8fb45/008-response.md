# 48d8fb45 • 008 • example_2 • investigate_coder

---
```python
"""
Extracts a 3x3 subgrid containing a cluster of yellow pixels from the input grid, preserving their relative positions, and removing any gray pixels.
"""

import numpy as np

def find_yellow_cluster(grid):
    # Find coordinates of all yellow pixels
    yellow_coords = np.argwhere(grid == 4)
    if yellow_coords.size == 0:
        return None, None
    
    # use a different method from find_objects, find bounds, but use the yellow coordinates to identify a center
    min_row = np.min(yellow_coords[:, 0])
    max_row = np.max(yellow_coords[:, 0])
    min_col = np.min(yellow_coords[:, 1])
    max_col = np.max(yellow_coords[:, 1])

    return yellow_coords, (min_row, max_row, min_col, max_col)

def get_subgrid_bounds(min_row, max_row, min_col, max_col):
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    top = center_row - 1
    bottom = center_row + 1
    left = center_col - 1
    right = center_col + 1
    return top, bottom, left, right

def transform(input_grid):
    # Find yellow pixels and their bounding box
    yellow_coords, bounds = find_yellow_cluster(input_grid)

    if yellow_coords is None:
       return np.zeros((3,3), dtype=int)

    min_row, max_row, min_col, max_col = bounds

    # get 3x3 subgrid bounds
    top, bottom, left, right = get_subgrid_bounds(min_row, max_row, min_col, max_col)
    # print(top, bottom, left, right)

    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Extract the subgrid and place it in the output grid.  Handle boundary conditions
    for r in range(max(0,top), min(input_grid.shape[0], bottom+1)):
      for c in range(max(0, left), min(input_grid.shape[1], right + 1)):
        if input_grid[r,c] == 4:
            output_row = r - top
            output_col = c - left
            output_grid[output_row, output_col] = input_grid[r,c]

    return output_grid
```
