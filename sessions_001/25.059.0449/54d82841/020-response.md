# 54d82841 • 020 • refine_coder

---
```python
"""
1.  **Copy Rows:** Copy all rows from the input grid to the output grid, up to but not including the last row.
2.  **Conditional Replacement (Last Row):** For the last row of the output grid, iterate through each column:
    *   If the pixel in the corresponding column of the *last* row of the *input* grid is white (0), check the pixel in the same column of the row *before* the last row of the *input* grid.
    *   If the pixel in the row before last is either azure (8) or magenta (6), change the corresponding pixel in the last row of the *output* grid to yellow (4).
    *   Otherwise, keep the pixel in the last row of the *output* grid the same as the corresponding pixel of the last row of the *input* grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input, but with the same dimensions
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Copy all rows except the last one
    for i in range(rows - 1):
        output_grid[i] = input_grid[i]

    # Modify the last row based on the row before last
    for c in range(cols):
        if input_grid[rows - 1, c] == 0:  # Check if the pixel in the last row of input is white
            if rows > 1 and (input_grid[rows - 2, c] == 8 or input_grid[rows - 2, c] == 6):  # Check row before last
                output_grid[rows - 1, c] = 4  # Change to yellow
            #else, the value should be copied, which it already has been

    return output_grid
```
