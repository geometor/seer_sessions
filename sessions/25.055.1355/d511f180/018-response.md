# d511f180 • 018 • refine_coder

---
```python
"""
The transformation rule operates on 3x3 grids. It identifies pixels of color 'gray' in the input grid. For each column, find the color of the top-most non-gray pixel. Then, replace any gray pixel in the leftmost column of the grid with the top-most non-gray colors that occur in the same column. All other pixels in the input grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if the grid is 3x3. If not, return the original grid.
    if rows != 3 or cols != 3:
        return output_grid

    # Iterate through each column.
    for j in range(cols):
      # Find the top-most non-gray pixel in the current column
      top_non_gray = None
      for i in range(rows):
          if input_grid[i,j] != 5:
              top_non_gray = input_grid[i,j]
              break #stop once first non-gray color found

      #replace gray pixel in first column with the top most color
      if top_non_gray is not None:
          for i in range(rows):
            if input_grid[i,0] == 5:
                output_grid[i,0] = top_non_gray

    return output_grid
```
