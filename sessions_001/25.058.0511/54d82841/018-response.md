# 54d82841 • 018 • refine_coder

---
```python
"""
1.  **Identify Source Row:** Locate the second-to-last row of the input grid.
2.  **Find Trigger Pixels:** Within the source row, identify the column indices of all white (0) pixels.
3.  **Identify Target Row:** Locate the last row of the input grid.
4.  **Apply Transformation:** For each column index identified in step 2, change the pixel in the target row at that column index to yellow (4). If no trigger pixels exist, the target row does not change.
5. **Output:** output is the modified grid.
"""

import numpy as np

def find_pixel_indices(row, color):
    """Finds the column indices of pixels of a specific color in a row."""
    indices = []
    for i, pixel in enumerate(row):
        if pixel == color:
            indices.append(i)
    return indices

def transform(input_grid):
    """
    Transforms the input grid by adding yellow pixels to the last row based on the
    positions of white pixels in the second-to-last row.
    """
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # 1. Identify Source Row: Locate the second-to-last row.
    source_row_index = rows - 2

    # 2. Find Trigger Pixels: Find white (0) pixels in the source row.
    source_row = output_grid[source_row_index]
    trigger_indices = find_pixel_indices(source_row, 0)

    # 3. Identify Target Row: Locate the last row.
    target_row_index = rows - 1

    # 4. Apply Transformation: Add yellow (4) pixels to the target row.
    for col_index in trigger_indices:
        output_grid[target_row_index, col_index] = 4

    # 5. Output: Return the modified grid.
    return output_grid
```
