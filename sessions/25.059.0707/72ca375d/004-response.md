# 72ca375d • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify the Target Object: Locate the contiguous region of magenta (6) pixels within the input grid.
2. Isolate with Padding: It looks like one row of 0's above and below the object of 6's are included and 1 column of 0's to the left and right of the object.
3. Extract: Create the output by cropping the selection found in step 2.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Color not found
    # find min and max row and col
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # 1. Identify the Target Object (magenta/6).
    object_bounds = find_object(input_grid, 6)

    if object_bounds is None:
        return [[]]

    min_row, max_row, min_col, max_col = object_bounds

    # 2. Isolate with Padding.
    padded_min_row = max(0, min_row - 1)
    padded_max_row = min(input_grid.shape[0], max_row + 2)
    padded_min_col = max(0, min_col - 1)
    padded_max_col = min(input_grid.shape[1], max_col + 2)

    # 3. Extract the padded region.
    output_grid = input_grid[padded_min_row:padded_max_row, padded_min_col:padded_max_col]
    
    return output_grid.tolist()
```
