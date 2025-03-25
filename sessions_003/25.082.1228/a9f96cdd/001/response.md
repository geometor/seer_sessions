```python
"""
1.  **Identify:** Locate all pixels with the color '2' (red) in the input grid.
2.  **Transform:** Based on the position type of color 2, replace color 2, and add colors.
    *    If red is in a corner, replace with three other colors.
        *    Top Left corner, replace with a 3.
        *    Top Right corner, replace with a 6.
        *    Bottom Left corner, replace with an 8.
        *     Bottom Right corner, replace with a 7.
    *   If red in an edge (not corner):
        *   Top replace red with 3, 6
        *   Bottom replace with 8, 7
        *   Right replace with 3
        *   Left replace with 8, 7.
3.  **Output:** Create a new grid with the same dimensions as the input grid, filled with '0' (white) as the background. Place the transformed numbers and colors in the new output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 2:
                if i == 0 and j == 0:  # Top Left
                    output_grid[i,j] = 3
                elif i == 0 and j == cols - 1:  # Top Right
                    output_grid[i,j] = 6
                elif i == rows - 1 and j == 0:  # Bottom Left
                    output_grid[i,j] = 8
                elif i == rows - 1 and j == cols - 1:  # Bottom Right
                    output_grid[i,j] = 7
                elif i == 0: # Top edge
                    output_grid[i,j] = 3
                    output_grid[i,j+1] = 6
                elif i == rows-1:
                    output_grid[i,j-1] = 8
                    output_grid[i,j] = 7
                elif j == cols-1:
                    output_grid[i-1,j] = 3
                elif j == 0:
                    output_grid[i+1,j] = 8
                    output_grid[i,j+1] = 7
    return output_grid
```