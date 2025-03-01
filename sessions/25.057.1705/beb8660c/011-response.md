# beb8660c • 011 • refine_coder

---
```python
"""
Vertically flips the positions of non-empty pixels in a grid, preserving empty spaces.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid_np[r, c] != 0:
                # Vertical Flip: new_row = total_rows - 1 - original_row
                new_row = rows - 1 - r
                output_grid[new_row, c] = input_grid_np[r, c]

    return output_grid.tolist()
```
