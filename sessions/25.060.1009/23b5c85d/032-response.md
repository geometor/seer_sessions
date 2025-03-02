# 23b5c85d • 032 • refine_coder

---
```python
"""
Locate the contiguous region of yellow (4) pixels in the input grid.  The definition of the yellow region is that every yellow pixel is either directly above, below, to the left, or the right of another yellow pixel. Determine the minimum and maximum row and column indices that encompass this yellow region. Create a new grid containing only the pixels within the boundaries. This will always form a rectangle, since it is defined by min/max row/col. Return the extracted sub-grid as output.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Return None if color not found
    # Calculate the bounding box.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of the yellow (4) region.
    min_row, max_row, min_col, max_col = find_object(input_grid, 4)
    
    if min_row is None:  # Handle case where yellow is not found
        return np.array([])

    # Extract the yellow region.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    return output_grid
```

