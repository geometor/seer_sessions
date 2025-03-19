# 54d82841 • 014 • example_3 • investigate_coder

---
```python
"""
Yellow pixels are added to the bottom row, mirroring the horizontal positions of white pixels in the second-to-last row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by adding yellow pixels to the last row based on the
    positions of white pixels in the second-to-last row.
    """
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # 1. Identify Target Row: Locate the second-to-last row (index rows - 2).
    target_row = rows - 2

    # 2. Find White Pixels: Find white pixels (value 0) in the target row.
    white_pixel_cols = []
    for col in range(cols):
        if output_grid[target_row, col] == 0:
            white_pixel_cols.append(col)

    # 3. Note Columns: The white_pixel_cols list now holds the column indices.

    # 4. Add Yellow Pixels: Add yellow (4) to the last row (rows - 1) at the recorded columns.
    for col in white_pixel_cols:
        output_grid[rows - 1, col] = 4

    # 5. If there are no white, we don't hit the loop, so don't add yellow
    # 6. Output Grid: The modified grid is the output.
    return output_grid
```

