# c1d99e64 • 006 • refine_coder

---
```python
"""
Copy all white (0) pixels from the input grid to the output grid.
Draw a red (2) cross (+) in the output grid, centered.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Calculate the center row and column indices.
    center_row = rows // 2
    center_col = cols // 2

    # Draw the red cross.  Iterate through rows and cols, setting to 2
    # only if it's the center row or center column.
    for r in range(rows):
        for c in range(cols):
            if r == center_row or c == center_col:
                output_grid[r,c] = 2

    # Copy 0's
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 0:
                output_grid[row,col] = 0

    return output_grid
```
