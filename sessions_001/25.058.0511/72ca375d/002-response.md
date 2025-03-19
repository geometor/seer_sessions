# 72ca375d • 002 • example_1 • investigate_coder

---
```python
"""
Extracts the largest magenta (6) colored rectangular region from the input grid and creates a new grid representing its bounding box, filling non-magenta pixels with white (0).
"""

import numpy as np

def find_largest_object(grid, color):
    """Finds the largest contiguous object of a given color."""
    labeled_grid, num_objects = ndimage.label(grid == color)
    if num_objects == 0:
        return None, None, None, None
    object_sizes = np.bincount(labeled_grid.ravel())
    largest_object_label = np.argmax(object_sizes[1:]) + 1
    rows, cols = np.where(labeled_grid == largest_object_label)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the largest magenta object and represents it as a 2D numpy array.
    """
    # Convert the input grid to a NumPy array
    input_np = np.array(input_grid)

    # Find the bounding box of the largest magenta (6) object
    min_row, max_row, min_col, max_col = find_largest_object(input_np, 6)
    
    if min_row is None:
        return []
    
    
    # initialize output
    output_np = np.zeros((max_row-min_row + 1, max_col - min_col + 1), dtype=int)

    # change output to 6 where magenta pixels exist
    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col + 1):
        if input_np[r][c] == 6:
          output_np[r-min_row][c-min_col] = 6
    
    return output_np.tolist()
```
