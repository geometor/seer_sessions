# 1b2d62fb • 017 • refine_coder

---
```python
"""
1.  **Identify the Blue Line:** Find the vertical line of blue pixels (value 1) in the input grid. If no such line exists, return the input grid.

2.  **Separate and Transform:** If a blue line is found:
    *   Iterate over all of the cells in the input.
    *   If the cell is to the left or right of the blue line, and its value is not 0, change the output grid cell in the same position to the value 8.
    *   fill all other cells in the output grid with 0

3. **Return result:** If there is no blue line in the input, the output matches the
   input.
"""

import numpy as np

def find_blue_line(grid_np):
    """Finds the column index of the vertical blue line (all 1s)."""
    for col_idx in range(grid_np.shape[1]):
        if np.all(grid_np[:, col_idx] == 1):
            return col_idx
    return -1

def transform(input_grid):
    """Transforms the input grid based on the blue line rule."""
    input_np = np.array(input_grid)
    blue_line_col = find_blue_line(input_np)

    # If no blue line, return the original grid
    if blue_line_col == -1:
        return input_grid

    rows, cols = input_np.shape
    output_grid = np.zeros((rows,cols), dtype=int)

    # Iterate through the grid and transform pixels
    for r in range(rows):
        for c in range(cols):
            if (c < blue_line_col or c > blue_line_col) and input_np[r, c] != 0:
                output_grid[r,c] = 8
            
    return output_grid.tolist()
```
