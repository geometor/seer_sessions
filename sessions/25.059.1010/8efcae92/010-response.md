# 8efcae92 • 010 • example_2 • investigate_coder

---
```python
"""
Extract a subgrid from the input, remove white pixels, and resize/condense it, 
preserving the relative positions of red and blue pixels.
"""

import numpy as np

def find_bounding_box(grid):
    #find rows and cols containing non-white pixels
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    #get min/max of row/col indices
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of non-white pixels
    min_row, max_row, min_col, max_col = find_bounding_box(input_grid)
    
    # Extract the subgrid within the bounding box
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Eliminate white pixels, keeping only red and blue
    subgrid_no_white = subgrid[subgrid != 0]

    #reshape to final size (this doesn't work)
    output_grid = subgrid_no_white.reshape(9,9)

    
    return output_grid
```
