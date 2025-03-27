"""
1.  **Identify Gray Rows:** Examine the input grid and identify rows that contain at least one gray (value 5) pixel.
2.  **Create Output Grid:** Create an output grid. The height is equal to the number of gray rows identified in step 1, and the width is always 3.
3.  **Iterate and Copy/Transform:** For each row identified in step 1, consider only the first three columns of the input grid.
    -   If a pixel in the selected input row and column is gray (5), copy a red (2) pixel to the corresponding position in the output grid.
    -   Otherwise, copy a black (0) pixel to the corresponding position in the output grid.
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