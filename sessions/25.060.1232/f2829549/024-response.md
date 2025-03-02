# f2829549 • 024 • refine_coder

---
```python
"""
Find the vertical blue line in the input grid. Extract the columns to the left of this blue line. Within these extracted columns, change any orange pixels to green.
"""

import numpy as np

def find_blue_line_column(grid):
    # Iterate through columns to find the one containing only blue (1) pixels.
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no blue line is found

def transform(input_grid):
    # Find the column index of the blue line.
    blue_line_column = find_blue_line_column(input_grid)

    # Initialize the output grid with the correct dimensions (same height, width up to blue line).
    output_grid = np.zeros((input_grid.shape[0], blue_line_column), dtype=int)
    
    # copy the grid up to blue line
    if (blue_line_column != -1):
        output_grid = input_grid[:, :blue_line_column].copy()

        # change any orange (7) to green(3)
        output_grid[output_grid == 7] = 3
    
    return output_grid
```

