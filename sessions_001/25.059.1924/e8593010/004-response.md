# e8593010 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Iterate** through each pixel in the input grid.
2.  **Identify** pixels with the color value 0 (white).
3.  **Change** the color of the white pixels based on their position within the grid:
    *   Change to blue (1) if the pixel is in the top left.
    *   Change to red (2) if the pixel is in the bottom right, center, or top right.
    *    Change to green (3) if the pixel is in the top or bottom row.
4. All other pixels colors that are not 0 remain the same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                if i <= 2 and j <= 2:
                    output_grid[i,j] = 1
                elif (i >= rows -3  or i <=2) and j>= cols -3:
                    output_grid[i, j] = 2
                elif i >= 4 and i <= rows-4 and j>= cols -3:
                     output_grid[i, j] = 2
                elif (i == 0 or i == rows -1) and ( j<=2 or j>= cols -3):
                    output_grid[i, j] = 3
                elif (i == 0 or i == rows -1):
                    output_grid[i,j] = 3
                elif (j == 0 and i <=2) or (j == cols-1 and i ==rows -2):
                    output_grid[i, j] = 3
                elif i >= 4 and i<= rows -4 and (j<=2):
                    output_grid[i, j] = 3
                

    return output_grid
```
