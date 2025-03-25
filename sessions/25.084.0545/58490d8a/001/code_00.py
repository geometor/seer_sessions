"""
1.  **Identify Target Colors:** Determine the colors present in the output grid (excluding 0, which represents the background).
2. **Scan and select**: scan the input grid and select only those colors that are the target colors.
3.  **Reduce Rows:** Group every three rows of the input grid, select the first row in each group, and put the group into a new grid.
4. **Condense and position:** Scan every section of 3 x 3 area in the first row of each row group and find the colors. Place those colored pixels into the new grid.
5.  **Output:** The resulting grid is the output.
"""

import numpy as np

def get_target_colors(output_grid):
    # Flatten the output grid and get unique colors, excluding 0
    return np.unique(output_grid[output_grid != 0])

def reduce_rows(input_grid):
  """Groups rows in sets of three and keeps only first of each group."""
  reduced_grid = []
  for i in range(0, len(input_grid), 3):
      reduced_grid.append(input_grid[i])
  return np.array(reduced_grid)

def transform(input_grid):
    input_grid = np.array(input_grid)
    
    reduced = reduce_rows(input_grid)
    
    # initialize output_grid
    output_grid = np.zeros((len(reduced), (len(reduced[0]) // 3) + (1 if len(reduced[0])%3 != 0 else 0) ), dtype=int)


    # Scan reduced and select target_colors.
    for row_idx, row in enumerate(reduced):
      for col_idx in range(0, len(row), 3):
          colors = row[col_idx: min(col_idx + 3, len(row))]
          target_colors = np.unique(colors[colors != 0])
          if (len(target_colors) > 0):
              output_grid[row_idx, col_idx//3] = target_colors[0] #place one colored pixel

    return output_grid.tolist()