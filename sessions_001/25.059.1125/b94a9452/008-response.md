# b94a9452 • 008 • refine_coder

---
```python
"""
1. Identify the Region of Interest (ROI): Find the smallest rectangular region within the input grid that completely encloses all non-zero pixels. This is the bounding box.
2. Extract the ROI: Extract the sub-grid defined by the bounding box.
3. Flip the ROI: Reverse the order of rows within the extracted sub-grid. Then, reverse the order of columns within the extracted sub-grid. This is equivalent to flipping the region both horizontally and vertically, or rotating it 180 degrees.
4. Output: The resulting flipped sub-grid is the output. If there are no non-zero pixels, the output is an empty grid.
"""

import numpy as np

def get_bounding_box(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify the Region of Interest (ROI)
    bounding_box = get_bounding_box(input_grid)
    if bounding_box is None:  # If no non-zero pixels
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # 2. Extract the ROI
    roi = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 3. Flip the ROI (both horizontally and vertically)
    output_grid = np.flip(roi) # Flip both rows and cols

    return output_grid.tolist()
```
