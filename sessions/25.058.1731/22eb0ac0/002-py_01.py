"""
1. **Identify Target Rows:** Scan the input grid to find rows that contain more than one non-zero pixel.
2. **Check for Replication:** If a row is identified, replicate the first color of the row to make the entire row the first color.
3. **Preserve other Rows:** All other rows, remain unchanged.
4. **Output**: A new grid is the final result
"""

import numpy as np

def find_rows_with_multiple_colors(grid):
    """Finds rows with more than one non-zero pixel."""
    rows = []
    for i, row in enumerate(grid):
        non_zero_pixels = [x for x in row if x != 0]
        if len(non_zero_pixels) > 1:
            rows.append(i)
    return rows

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)  # Initialize output as a copy
    rows_to_transform = find_rows_with_multiple_colors(input_grid)

    for row_index in rows_to_transform:
      first_color = input_grid[row_index][0]
      # find the first non zero pixel in the input grid
      for i, pixel in enumerate(input_grid[row_index]):
        if pixel != 0:
          first_color = pixel
          break;
      # set the output grid as the first color
      output_grid[row_index, :] = first_color

    return output_grid