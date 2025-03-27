```python
"""
1.  **Identify Gray Rows:** Examine the input grid and find all rows that contain at least one gray pixel.
2.  **Create Output Grid:** Create an output grid with a height equal to the number of rows identified in step 1 and a width of 3.
3. **Iterate and copy/transform pixels**: Consider only the first 3 columns of the input, copy the grid values from input rows which have gray pixels to the output, transform gray(5) to red(2) and any other color to black(0).
"""

import numpy as np

def transform(input_grid):
    # Identify Gray Rows
    gray_rows = np.any(input_grid == 5, axis=1)
    gray_row_indices = np.where(gray_rows)[0]
    num_gray_rows = len(gray_row_indices)

    # Create Output Grid
    output_grid = np.zeros((num_gray_rows, 3), dtype=int)

    # Iterate through the identified rows and the first 3 columns of input.
    for i, row_index in enumerate(gray_row_indices):
      for j in range(min(3, input_grid.shape[1])):  # Limit to first 3 columns
          # transform pixels
          if input_grid[row_index, j] == 5:
              output_grid[i, j] = 2
          else:
              output_grid[i,j] = 0

    return output_grid
```