# 8d510a79 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the central gray line:** Locate the horizontal line of gray (5) pixels at row 4 (index 3).
2.  **Iterate the columns.** Iterate through each of the columns.
3.  **Duplicate above and below.** For each colored pixel, going from the grey line to the edges of the grid, duplicate the current color to the output grid. For example, looking at the first column, from the grey line to the top: white, white, red, white -> write to the ouput, starting at the grey line: white, red, white, white. Then repeat for the other side of the grey line.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    gray_line_row = 3  # The gray line is at row index 3

    for j in range(input_grid.shape[1]):
        # Duplicate from gray line to top edge
        for i in range(gray_line_row -1, -1, -1):
          output_grid[gray_line_row - (gray_line_row - i), j] = input_grid[i,j]
        # Duplicate from gray line to bottom edge
        for i in range(gray_line_row + 1, input_grid.shape[0]):
           output_grid[gray_line_row + (i - gray_line_row),j] = input_grid[i,j]
    return output_grid
```
