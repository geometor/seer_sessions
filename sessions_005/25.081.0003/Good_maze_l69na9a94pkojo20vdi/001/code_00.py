"""
1.  **Identify Trigger and Target:** Locate all yellow (4) and red (2) pixels within the input grid.
2.  **Determine the area between yellow (4) pixels, considering rows and columns.** A yellow pixel will be either at the start or the end of the row or column.
3.  **Replace with Azure:** Within that range of rows and columns, replace all red (2) pixels by Azure (8).
4. **Background Preservation**: Black Pixels (0) remain in place, unchanged.
"""

import numpy as np

def get_positions(grid, color):
    positions = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                positions.append((r_idx, c_idx))
    return positions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid).astype(int)
    yellow_positions = get_positions(input_grid, 4)
    red_positions = get_positions(input_grid, 2)

    # change output pixels based on rows
    for r_idx, row in enumerate(input_grid):
      yellow_in_row = [c_idx for r_idx2, c_idx in yellow_positions if r_idx2 == r_idx]
      if len(yellow_in_row) > 0 :
        min_yellow = min(yellow_in_row)
        max_yellow = max(yellow_in_row)
        for c_idx in range(len(row)):
          if input_grid[r_idx, c_idx] == 2:
            if (len(yellow_in_row) == 1 and c_idx >= min_yellow) or (min_yellow <= c_idx <= max_yellow):
               output_grid[r_idx, c_idx] = 8
    
    #change output pixels based on columns:
    for c_idx in range(len(input_grid[0])):
      yellow_in_col = [r_idx for r_idx, c_idx2 in yellow_positions if c_idx2 == c_idx]
      if len(yellow_in_col) > 0:
        min_yellow = min(yellow_in_col)
        max_yellow = max(yellow_in_col)
        for r_idx in range(len(input_grid)):
          if input_grid[r_idx, c_idx] == 2:
            if (len(yellow_in_col) == 1 and r_idx >= min_yellow) or (min_yellow <= r_idx <= max_yellow):
              output_grid[r_idx, c_idx] = 8


    return output_grid