# d037b0a7 • 004 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the Key Colors: Find all cells that are not white (0).
2. Propagation of the Dominant color, magenta (6): Iterate to fill all cells that are white to magenta if the cell to its left is magenta.
3. Fill with the Top-Left Color: All the remaining white cells (0) will be the same color of the top-left cell.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the top-left color
    top_left_color = output_grid[0, 0]

    # Iterate through the grid
    for i in range(rows):
        for j in range(cols):
            # Propagation of magenta (6)
            if j > 0 and output_grid[i, j-1] == 6:
                if output_grid[i,j] == 0:
                    output_grid[i, j] = 6
            # Fill remaining 0s with the top-left color
            elif output_grid[i,j] == 0:
                output_grid[i,j] = top_left_color


    return output_grid
```
