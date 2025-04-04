# 99b1bc43 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Locate connected regions of blue (1), red(2), and yellow(4) pixels in the input grid.

2.  **Create the output grid:** A grid of 4x4 is created.

3.  **Mark locations:** If a pixel of value 1, 2, or 4 appears in the input grid, mark its relative position with green (3) in the output grid.
4.  Fill the rest with 0s.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to highlight regions of blue, red and yellow with green and the rest with white."""

    input_array = np.array(input_grid)
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the first 4 rows, checking for 1, 2 and 4 values.
    for i in range(4):
      for j in range(4):
        if input_array[i][j] == 1:
            output_grid[i][j] = 3
    
    # Iterate through rows containing the yellow region
    for i in range(4,5): #Row containing the yellow color
       for j in range(4):
          if input_array[i][j] == 4:
            row_index = i-4+2
            if row_index >=0 and row_index <4:
              output_grid[row_index][j] = 3

    # Iterate through the bottom rows (containing the red regions), starting from the 7th row of the input.
    for i in range(6, 9):
      for j in range(4):
          if input_array[i][j] == 2:
              row_index = i - 6 + 2
              #print(i,row_index)
              if row_index>=0 and row_index < 4:
                output_grid[row_index][j] = 3


    return output_grid.tolist()
```
