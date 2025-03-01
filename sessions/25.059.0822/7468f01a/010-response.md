# 7468f01a • 010 • refine_coder

---
```python
"""
1.  **Identify the bounding box:** Find the smallest rectangle within the input grid that encompasses all yellow (4) pixels.
2.  **Crop:** Extract the region of the input grid defined by the bounding box in step 1.
3. **Output the bounding box:** The cropped region is the output grid.  If no yellow pixels are present, return an empty grid.
"""

import numpy as np

def find_yellow_bounding_box(grid):
    # Find row and column indices of all yellow (4) pixels
    rows, cols = np.where(grid == 4)
    
    # If there are no yellow pixels, return None
    if len(rows) == 0:
        return None
    
    # Calculate min and max row/col to define the bounding box
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of yellow pixels
    bounding_box = find_yellow_bounding_box(input_grid)
    
    # Handle cases where there are no yellow pixels
    if bounding_box is None:
        return np.array([])  # Return empty grid
    
    min_row, max_row, min_col, max_col = bounding_box

    # Crop the input grid to the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid
```
