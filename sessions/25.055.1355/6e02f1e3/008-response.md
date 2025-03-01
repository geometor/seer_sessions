# 6e02f1e3 • 008 • example_2 • investigate_coder

---
```python
"""
Transforms a 3x3 input grid into a 3x3 output grid, where:
- Green (3) pixels in the top row become white (0), except the last one becomes gray (5).
- Yellow (4) pixels in the left column become white (0), except the last one becomes gray (5).
- Red (2) pixels in the last two rows become white (0), except those at the edges in the last row and at the top right become gray (5).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with all white (0) pixels.
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Apply color transformation rules.
            if input_grid[i, j] == 3 and i == 0:  # Green in the top row
                output_grid[i, j] = 0 if j < 2 else 5
            elif input_grid[i, j] == 4 and j == 0:  # Yellow in the left column
                output_grid[i, j] = 0 if i < 2 else 5
            elif input_grid[i, j] == 2 and i > 0:   # Red in last two rows
                if (i==2 and j==0):
                    output_grid[i,j] = 5
                elif (i == 1 and j == 2):
                    output_grid[i, j] = 5;
                else:
                    output_grid[i,j] = 0
    return output_grid
```
