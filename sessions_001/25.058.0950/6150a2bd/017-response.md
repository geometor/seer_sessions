# 6150a2bd • 017 • refine_coder

---
```python
"""
1.  **Zero Preservation:** All pixels with a value of 0 (white) in the input grid remain unchanged in the output grid.

2.  **Non-Zero Pixel Movement:**
    *   All non-zero pixels in the input grid are moved to the far-right column (column index 9) of the output grid.
    *   The non-zero pixel in column 0 moves to the last column, and one row up.
    *   All other colored pixels disappear.
3. Blank cells created by moving the objects are filled with 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the non-zero pixel in the first column (if any)
    left_pixel_pos = None
    for r in range(rows):
        if input_grid[r, 0] != 0:
            left_pixel_pos = (r, 0)
            break

    # Move the left-most pixel to the top-right, one row up
    if left_pixel_pos:
        new_row = left_pixel_pos[0] - 1
        output_grid[new_row, cols - 1] = input_grid[left_pixel_pos]
        
    return output_grid
```
