# 1b2d62fb • 002 • example_5 • investigate_coder

---
```python
"""
1.  **Identify the Blue Column:** Locate the vertical column of blue (1) pixels within the input grid. Note its horizontal position (column index).
2. **Create output skeleton:** Create a new output grid. The output grid has the same number of rows of input grid, and has a fixed width of 3 columns. Initialize it by value 0.
3.  **Map Blue Column to Azure:**
    *   Iterate the rows of input grid, using the row index.
    *   If exists any blue pixel in the input row, put an azure pixel (8) in the output grid.
    * The azure pixel position is given from two factors: the relative position respect the blue column, and the borders of a 3x3 subgrid around the relative postion.
4.  **Fill Remaining Pixels:** All other pixels in the output grid, not part of azure mapping, remain white (0).
"""

import numpy as np

def find_blue_column(grid):
    # Find the column index where blue (1) pixels are present.
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no blue column is found

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((input_grid.shape[0], 3), dtype=int)
    
    # Find the blue column
    blue_column_index = find_blue_column(input_grid)

    if blue_column_index == -1:
        return output_grid # returns all zeros if there is no blue column

    # Map Blue column to Azure
    for i in range(input_grid.shape[0]):
      if 1 in input_grid[i,:]:
        # determine the position of azure pixel in output, given relative postion and borders
        if blue_column_index == 0:
            output_grid[i,0] = 8
        elif blue_column_index == input_grid.shape[1]-1:
            output_grid[i,2] = 8
        elif 1 in input_grid[i,:]:
          if input_grid[i,blue_column_index-1] != 0 and input_grid[i,blue_column_index+1] != 0:
              output_grid[i,1] = 8
              output_grid[i,2] = 8
          elif input_grid[i,blue_column_index-1] == 0 and input_grid[i,blue_column_index+1] == 0:
            output_grid[i,1] = 8
          elif input_grid[i,blue_column_index-1] != 0 and input_grid[i,blue_column_index+1] == 0 :
              output_grid[i,2] = 8
          elif input_grid[i,blue_column_index-1] == 0 and input_grid[i,blue_column_index+1] != 0:
              output_grid[i,0] = 8
            
    return output_grid
```
