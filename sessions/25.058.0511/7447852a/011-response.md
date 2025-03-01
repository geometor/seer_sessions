# 7447852a • 011 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all red (2) pixels within the input grid.
2.  **Row-wise Yellow Placement:** For each row containing a red pixel:
    * Find the position of the leftmost white pixel before the first red.
    * Change this white pixel to yellow.
3. **Column-wise Yellow Placement:** For each column containing a red pixel,
     *   Find the position of the upmost white pixel before the first red.
       *   Change this white pixel to yellow.
4.  **All other pixels:** Remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on red pixel positions, placing yellow pixels
    to the left of the first red pixel in each row, and above the first
    red pixel in each column.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Row-wise Yellow Placement
    for r in range(rows):
        red_indices = np.where(input_grid[r, :] == 2)[0]
        if len(red_indices) > 0:
            first_red_index = red_indices[0]
            for c in range(first_red_index):
                if input_grid[r,c] == 0:
                    output_grid[r,c] = 4
                    break # only place one yellow per row

    # Column-wise Yellow Placement
    for c in range(cols):
        red_indices = np.where(input_grid[:, c] == 2)[0]
        if len(red_indices) > 0:
            first_red_index = red_indices[0]
            for r in range(first_red_index):
                if input_grid[r,c] == 0:
                    output_grid[r,c] = 4
                    break # only place one yellow per column

    return output_grid
```
