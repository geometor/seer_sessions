"""
The input grid is expanded by mirroring the non-zero pixels both horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find non-zero pixels
    non_zero_pixels = [(r, c, input_grid[r, c]) for r in range(rows) for c in range(cols) if input_grid[r, c] != 0]

    # Determine output grid dimensions (this logic seems consistent across examples)
    
    # Count sections and calculate the spaces between in the input
    non_zero_cols = np.any(input_grid != 0, axis=0)
    num_cols_sections = np.sum(non_zero_cols)
    spaces_between_cols = 0
    if(num_cols_sections > 1):
        first_col_section = -1
        last_col_section = -1
        for i in range(0, len(non_zero_cols)):
            if non_zero_cols[i] and first_col_section == -1 :
                first_col_section = i
            if non_zero_cols[i]:
                last_col_section = i
        spaces_between_cols = (last_col_section - first_col_section) - (num_cols_sections -1)

    non_zero_rows = np.any(input_grid != 0, axis=1)
    num_rows_sections = np.sum(non_zero_rows)    
    spaces_between_rows = 0
    if (num_rows_sections > 1) :    
      first_row_section = -1
      last_row_section = -1
      for i in range(0, len(non_zero_rows)):
        if non_zero_rows[i] and first_row_section == -1:
          first_row_section = i
        if non_zero_rows[i]:
          last_row_section = i
      spaces_between_rows = (last_row_section - first_row_section) - (num_rows_sections - 1)
    
    output_rows = (rows * 2) + spaces_between_rows
    output_cols = (cols * 2) + spaces_between_cols

    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Replicate and mirror the input grid
    # Top-left corner
    output_grid[:rows, :cols] = input_grid

    # Mirror horizontally
    output_grid[:rows, (cols + spaces_between_cols):] = np.fliplr(input_grid)

    # Mirror vertically
    output_grid[(rows + spaces_between_rows):, :cols] = np.flipud(input_grid)

    # Mirror both
    output_grid[(rows + spaces_between_rows):, (cols + spaces_between_cols):] = np.flipud(np.fliplr(input_grid))


    return output_grid.tolist()