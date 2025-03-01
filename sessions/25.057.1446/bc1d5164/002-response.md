# bc1d5164 • 002 • example_1 • investigate_coder

---
```python
"""
Extracts a rectangular subgrid from the input grid. The subgrid is defined as the largest
rectangular block containing azure (8) pixels, surrounded by a continuous border of white (0) pixels.
"""

import numpy as np

def find_bounding_box(grid):
    # Find coordinates of non-white pixels
    coords = np.argwhere(grid != 0)
    if coords.size == 0:  # Handle case where there are no non-white pixels
      return None

    # Find min and max row/col to define bounding box
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    
    # Find the bounding box of the azure region
    top_left, bottom_right = find_bounding_box(input_grid)
    
    # Check if the region is valid per the specs (surrounded by 0).
    # Expand the bounding box by one in each direction to check border.
    expanded_top_left = (max(0, top_left[0] - 1), max(0, top_left[1] - 1))
    expanded_bottom_right = (min(input_grid.shape[0] -1, bottom_right[0] + 1), min(input_grid.shape[1]-1, bottom_right[1] + 1))
    
    border_slice = input_grid[expanded_top_left[0]:expanded_bottom_right[0]+1, expanded_top_left[1]:expanded_bottom_right[1]+1]
    
    inner_slice = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    # create border mask, 1 if on the border, 0 if not
    border_mask = np.ones(border_slice.shape, dtype=bool)
    border_mask[1:-1, 1:-1] = False
   
    # if the border is all 0, we are good!
    if np.all(border_slice[border_mask] == 0):
        output_grid = inner_slice
    else:
        output_grid = inner_slice

    return output_grid.tolist()
```
