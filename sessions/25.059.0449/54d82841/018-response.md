# 54d82841 • 018 • refine_coder

---
```python
"""
1. Copy Rows: Copy the first four rows (indices 0-3) of the input grid directly to the output grid.
2. Conditional Replacement: For the last row (index 4) of the output grid, iterate through each column:
    *   If the pixel in the input grid's last row is white (0), check the pixel in the same column of row 2 (index 2) of the input grid.
    *   If the pixel in row 2 is either azure (8) or magenta (6), change the corresponding pixel in the output grid's last row to yellow (4).
    *   Otherwise, keep the pixel in the output grid's last row the same as the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Copy the first four rows
    for i in range(4):
        output_grid[i] = input_grid[i]
    
    # Modify the last row (index 4) based on row 2.
    for c in range(cols):
      if input_grid[rows-1,c] == 0:  # Check if the pixel in the last row is white
          if input_grid[2,c] == 8 or input_grid[2,c] == 6:  # Check if the pixel in row 2 is azure or magenta
              output_grid[rows - 1, c] = 4  # Change to yellow

    return output_grid
```
