# 1cf80156 • 002 • example_3 • investigate_coder

---
```python
"""
1. **Identify the colored object:** Locate the contiguous block of non-zero pixels within the input grid. This defines the region of interest.
2. **Extract the bounding box:** Determine the minimum and maximum row and column indices that enclose the colored object. This defines a rectangular subgrid.
3. **Create the output grid** Create new grid from the bounding box.
"""

import numpy as np

def find_object(grid):
    # Find the bounding box of the non-zero elements in the grid.
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty object case
        return (0, 0, 0, 0)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the bounding box of the object
    min_row, max_row, min_col, max_col = find_object(input_grid)

    # Extract the object using the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    return output_grid.tolist()
```
