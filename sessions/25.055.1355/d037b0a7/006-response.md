# d037b0a7 • 006 • refine_coder

---
```python
"""
1.  **Locate Subgrid**: Identify the 2x2 subgrid located at the bottom-right corner of the input grid.
2.  **Iterate**: Examine each cell within this 2x2 subgrid.
3.  **Conditional Fill**:
    *   If the current cell's color is white (0), replace the color of adjacent cells from Input Edges.

4.  **Preservation**: The cell at the top-left corner of the entire grid remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Fill the bottom right 2x2 subgrid
    for i in range(rows - 2, rows):
        for j in range(cols - 2, cols):
            if output_grid[i,j] == 0:
                if i == rows-2 and j == cols -2 :
                  if input_grid[i,j+1] != 0:
                     output_grid[i, j] = input_grid[i,j+1]
                elif i == rows-2 and j == cols -1:
                    if input_grid[i,j] !=0:
                       output_grid[i,j] = input_grid[i,j]

                elif i == rows-1 and j == cols-2:
                    if input_grid[i-1,j+1] !=0:
                       output_grid[i,j] = input_grid[i-1,j+1]
                    elif input_grid[i,j+1] != 0:
                         output_grid[i,j] = input_grid[i,j+1]
                    elif input_grid[i-1,j] != 0:
                       output_grid[i, j] = input_grid[i-1,j]


                elif i == rows -1 and j == cols-1 :
                    if input_grid[i-1,j-1] != 0:
                        output_grid[i,j] = input_grid[i-1,j-1]
                    elif input_grid[i,j-1] !=0:
                        output_grid[i,j] = input_grid[i,j-1]
                    elif input_grid[i-1,j] != 0:
                        output_grid[i,j] = input_grid[i-1,j]


    return output_grid
```
