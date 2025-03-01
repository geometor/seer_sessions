# 8d510a79 • 012 • refine_coder

---
```python
"""
1.  **Check for a Horizontal Gray Line:** Examine the input grid to determine if there's a row composed entirely of gray (value 5) pixels.
2.  **If a Gray Line Exists:**
    *   Perform a vertical reflection (mirroring) of the colors around this gray line. For each column, copy the colors from above the gray line to below it, and vice-versa, maintaining the gray line's position.
3.  **If No Gray Line Exists:** The output is identical to the input.
"""

import numpy as np

def find_gray_line(grid):
    """Finds the row index of a horizontal gray line, if it exists."""
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1  # Return -1 if no gray line is found

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    gray_line_row = find_gray_line(input_grid)

    if gray_line_row != -1:
        # Perform vertical reflection
        for j in range(input_grid.shape[1]):
            for i in range(gray_line_row - 1, -1, -1):
                output_grid[gray_line_row - (gray_line_row - i), j] = input_grid[i, j]
            for i in range(gray_line_row + 1, input_grid.shape[0]):
                output_grid[gray_line_row + (i - gray_line_row), j] = input_grid[i, j]
    else:
        # Output is identical to input
        pass # output_grid is already a copy of input_grid

    return output_grid
```

