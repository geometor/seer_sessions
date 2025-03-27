```python
"""
1.  **Find Gray Rows:** Identify the rows in the input grid that contain gray (5) pixels. Determine the minimum and maximum row indices among those rows.

2.  **Determine the output columns:** The output grid has three columns, starting from the zeroth column of the input.

3.  **Create Output Grid:** Construct an output grid with a height equal to (max_row - min_row + 1) and width 3.

4.  **Populate Output Grid:** Iterate through the cells bounded by the calculated rows (inclusive) and the first 3 columns of the input grid:
    *   If a cell within the subgrid in the input has gray color (5), set corresponding the cell in the output grid to red (2).
    *   Otherwise, set the cell in the output grid to black(0).

5.  **Return:** The resulting output grid is the transformed output.
"""

import numpy as np

def transform(input_grid):
    # Find the rows containing gray (5) pixels.
    gray_rows = np.any(input_grid == 5, axis=1)

    # Get the indices of the rows with gray pixels.
    gray_row_indices = np.where(gray_rows)[0]

    # Determine the minimum and maximum row indices.
    if gray_row_indices.size > 0:
      min_row = np.min(gray_row_indices)
      max_row = np.max(gray_row_indices)
    else:
      min_row = 0
      max_row = -1 # return empty array in this case
    
    # Create the output grid.
    output_height = max_row - min_row + 1
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid.
    for i in range(output_height):
      for j in range(output_width):
        if min_row + i < input_grid.shape[0] and j < input_grid.shape[1]: # prevent out of bounds errors
              if input_grid[min_row + i, j] == 5:
                  output_grid[i, j] = 2
              else:
                  output_grid[i,j] = 0
        else:
          output_grid[i,j] = 0
    return output_grid
```