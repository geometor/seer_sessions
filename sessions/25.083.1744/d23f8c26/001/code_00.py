"""
1. **Identify the Target Column:** Find the column in the input grid that has non-zero color and has the maximum number of unique values (all different colors).
2. **Filter Pixels:** Iterate through the entire input grid.
3. **Preserve or Blank:**
    - If a pixel is in the target column AND the pixel is not 0: Keep its original color value in the output grid.
    - Otherwise, if the pixel is not in the target column, but it is not a zero, set its color to black (0) in the output grid.
    - All pixels that are original zero, should stay zero.
"""

import numpy as np

def _find_target_column(input_grid):
    """Finds the column with the most unique non-zero colors."""
    max_unique_count = -1
    target_column = -1
    for j in range(len(input_grid[0])):
        column_values = []
        for i in range(len(input_grid)):
          if input_grid[i][j] != 0:
            column_values.append(input_grid[i][j])
        unique_count = len(set(column_values))
        if unique_count > max_unique_count:
            max_unique_count = unique_count
            target_column = j
    return target_column

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid with all zeros.
    output_grid = np.zeros_like(input_grid)

    # Find the target column.
    target_column = _find_target_column(input_grid)

    # Iterate through the input grid and apply the transformation.
    for i in range(len(input_grid)):
        for j in range(len(input_grid[0])):
            if j == target_column and input_grid[i][j] !=0:
                output_grid[i][j] = input_grid[i][j]
            elif input_grid[i][j]!=0:
                output_grid[i][j] = 0
            else:
                output_grid[i][j] = 0 # needed to be explicit

    return output_grid