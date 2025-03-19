# d406998b • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Initialization:** Start with the input grid.
2.  **Gray to Green conversion**: Iterate through each cell of the input grid.
    * If a pixel on the top row is white(0), and the very next pixel to right diagonally downwards is also white(0), change this top row pixel to green(3)
3.  **White to green conversion**: Iterate row by row.
    *   If a pixel on the leftmost column is white (0) and the pixel diagonally to its bottom right is also 0, change color to 3(green).
    *   If any white(0) pixel on any other column has a white(0) pixel on both of its sides, it transforms to green(3).
4.  **Copy Unchanged:** All other pixels, including original gray(5) that don't meet any of the above condition remains gray(5). Pixels that are not changed are copied directly from the input to the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Gray to Green conversion (top row, diagonal check)
            if r == 0 and input_grid[r][c] == 0:
                if r + 1 < rows and c + 1 < cols and input_grid[r+1][c+1] == 0:
                    output_grid[r][c] = 3
            # White to green conversion (leftmost column, diagonal check)
            elif c == 0 and input_grid[r][c] == 0:
                if r + 1 < rows and c + 1 < cols and input_grid[r+1][c+1] == 0 :
                    output_grid[r][c] = 3

            # White to Green - Horizontal
            elif input_grid[r][c] == 0:
                if c>0 and c < cols - 1 and input_grid[r][c-1] == 0 and input_grid[r][c+1] == 0:
                     output_grid[r][c] = 3

    return output_grid
```
