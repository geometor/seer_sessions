# d406998b • 018 • refine_coder

---
```python
"""
1.  **Initialization:** Start with the input grid.
2.  **Top Row Transformation:** Iterate through the top row. If a white pixel (0) is immediately to the left of a grey pixel (5), change the white pixel to green (3).
3.  **Downward Propagation (Green):** For all subsequent rows, if a white pixel (0) is directly below a green pixel (3), change the white pixel to green (3).
4.  **Downward and Left Propagation of 3 from 5:** if a while pixel (0) is directly below and one column to the left of a grey pixel(5), change the white pixel to green (3).
5.  **Grey (5) Remains:** Grey pixels (5) do not change.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Top Row Transformation
    for c in range(cols):
        if output_grid[0, c] == 0:
            if c + 1 < cols and output_grid[0, c + 1] == 5:
                output_grid[0, c] = 3

    # Downward Propagation and Left boarder propagation
    for r in range(1, rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                if output_grid[r - 1, c] == 3:
                    output_grid[r, c] = 3
                elif c > 0 and output_grid[r-1, c-1] == 5:
                    output_grid[r,c] = 3
    
    return output_grid
```
