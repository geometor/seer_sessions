# b94a9452 • 004 • example_1 • investigate_coder

---
```python
"""
Find the smallest rectangular region within the input grid that encompasses all non-zero pixels.
Extract that region.
Invert/flip the colors within the extracted region.
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

    # 3. Invert (Transpose in this case since the shapes are square)
    output_grid = roi.T

    return output_grid.tolist()
```
