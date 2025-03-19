# 4c5c2cf0 • 020 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying a blue (1) cluster in the input grid,
replicating it horizontally, and positioning the copy to the right of the original,
while keeping the azure (8) cluster and white (0) pixels unchanged.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Calculate the bounding box.
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()

    object_block = grid[min_row:max_row+1, min_col:max_col+1]
    
    return object_block, min_row, min_col, max_col

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the blue (1) object.
    blue_object, min_row, min_col, max_col = find_object(input_grid, 1)

    if blue_object is not None:
      # determine the size of the blue object block
      h, w = blue_object.shape

      # reflect the blue object and merge
      for r in range(h):
        for c in range(w):
          if blue_object[r,c]==1:
            # mirroring is complex
            # first copy blue pixels, preserving all original
            output_grid[min_row + r , max_col + 1 + c] = 1
            # ensure that copies are adjoined
            # example output shows that the copy mirrors the original
            if c>0 and blue_object[r, c-1] == 1:
              output_grid[min_row + r, max_col+c] = 1
            if r>0 and blue_object[r-1, c] == 1:
              output_grid[min_row + r -1, max_col+1+c] = 1
            if r+min_row < input_grid.shape[0]-1:
              output_grid[min_row + r +1, max_col+1+c] = 1

    return output_grid
```
