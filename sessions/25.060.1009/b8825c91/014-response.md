# b8825c91 • 014 • refine_coder

---
```python
"""
1. Identify Horizontal Lines: Scan each row of the input grid to identify contiguous horizontal lines of yellow (4) pixels. A line must have more than one pixel.
2. Check Preceding Row: For each identified yellow line, check the pixels directly above it in the preceding row.
3. Conditional Transformation:
    *   If the yellow line is in the top row (row 0), change all pixels in that line to blue (1).
    *   If the yellow line is not in the top row, and *none* of the pixels directly above it are yellow (4), change all pixels in the yellow line to blue (1).
    *   Otherwise, leave the yellow line unchanged.
4. Other Pixels: Leave all other pixels in the grid unchanged.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    """
    Finds contiguous horizontal lines of a specified color.
    Returns a list of (row, start_col, end_col) tuples.
    """
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = -1
        for c in range(cols):
            if grid[r, c] == color:
                if start_col == -1:
                    start_col = c
            elif start_col != -1:
                if c - start_col > 1:
                    lines.append((r, start_col, c - 1))
                start_col = -1
        if start_col != -1 and cols - start_col > 1:  # Check for line at the end of the row
            lines.append((r, start_col, cols - 1))
    return lines

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    yellow_lines = find_horizontal_lines(input_grid, 4)

    for row, start_col, end_col in yellow_lines:
        if row == 0:  # Top row
            output_grid[row, start_col:end_col+1] = 1
        else:  # Check preceding row
            above_is_yellow = False
            for c in range(start_col, end_col + 1):
                if input_grid[row - 1, c] == 4:
                    above_is_yellow = True
                    break
            if not above_is_yellow:
                output_grid[row, start_col:end_col+1] = 1

    return output_grid
```
