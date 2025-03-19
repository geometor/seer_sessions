# e8593010 • 008 • refine_coder

---
```python
"""
1.  **Iterate** through each cell (pixel) in the input grid.
2.  **Identify** cells with the color white (value 0).
3.  **Change** the color of white cells based on their position:
    *   **Top-Left Corner:** If a white cell is within the 3x3 top-left corner of the grid, change its color to blue (1).
    *   **Top-Right Corner:** If a white cell is within the 3x3 top-right corner of the grid, change its color to red (2).
    *   **Bottom-Left Corner:** If a white cell is within the 3x3 bottom-left corner of the grid, change its color to green (3).
    *   **Bottom-Right Corner:** If a white cell is within the 3x3 bottom-right corner of the grid, change its color to red (2).
    * **Top/Bottom Border:** If a white cell is in the top-most or bottom-most row of the grid, change its color to green(3).
4.  **Preserve Other Colors:** If a cell's color is not white, its color remains unchanged in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:  # Check if the cell is white
                # Top-Left Corner
                if i < 3 and j < 3:
                    output_grid[i, j] = 1
                # Top-Right Corner
                elif i < 3 and j >= cols - 3:
                    output_grid[i, j] = 2
                # Bottom-Left Corner
                elif i >= rows - 3 and j < 3:
                    output_grid[i, j] = 3
                # Bottom-Right Corner
                elif i >= rows - 3 and j >= cols - 3:
                    output_grid[i, j] = 2
                #Top/Bottom Border
                elif i == 0 or i == rows -1:
                    output_grid[i,j] = 3

    return output_grid
```
