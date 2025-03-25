"""
The transformation involves identifying a section of the input grid (either rows or columns) that undergoes a "mirroring" operation and color remapping. The mirrored section's location in the output depends on whether it was originally on the left/right (for columns) or top/bottom (for rows).  The colors within this mirrored section are swapped based on a specific rule for each example.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to find color swaps
    def find_color_swaps(input_grid, output_grid):
        swaps = {}
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] != output_grid[r, c]:
                    if input_grid[r, c] not in swaps:
                        swaps[input_grid[r, c]] = output_grid[r, c]
        return swaps

    # Helper Function for column mirroring
    def mirror_columns(input_grid, output_grid):
        num_cols_changed = 0
        first_changed_col = -1
        
        # count differences
        for j in range(cols):
           if not np.array_equal(input_grid[:, j], output_grid[:, j]):
              num_cols_changed += 1
              if first_changed_col == -1:
                 first_changed_col = j

        # if there are differences
        if num_cols_changed > 0:
            swaps = find_color_swaps(input_grid, output_grid)
            
            # check if leftmost
            if first_changed_col == 0:
              for j in range(num_cols_changed):
                for i in range(rows):
                  if input_grid[i,j] in swaps:
                    output_grid[i,cols - num_cols_changed + j] = swaps[input_grid[i, j]]
                  else:
                    output_grid[i,cols - num_cols_changed + j] = input_grid[i, j]
            # must be rightmost
            else:
              for j in range(num_cols_changed):
                for i in range(rows):
                  if input_grid[i,cols - num_cols_changed + j] in swaps:
                    output_grid[i,j] = swaps[input_grid[i, cols - num_cols_changed + j]]
                  else:
                    output_grid[i,j] = input_grid[i,cols - num_cols_changed + j]

            return True

        return False
    
    # mirror rows
    def mirror_rows(input_grid, output_grid):
        
        num_rows_changed = 0
        first_changed_row = -1

        # count differences
        for i in range(rows):
            if not np.array_equal(input_grid[i, :], output_grid[i, :]):
              num_rows_changed += 1
              if first_changed_row == -1:
                first_changed_row = i

        # if differences
        if num_rows_changed > 0:
            swaps = find_color_swaps(input_grid, output_grid)
            # check if top
            if first_changed_row == 0:
              for i in range(num_rows_changed):
                for j in range(cols):
                  if input_grid[i,j] in swaps:
                    output_grid[rows - num_rows_changed + i, j] = swaps[input_grid[i, j]]
                  else:
                    output_grid[rows - num_rows_changed + i,j] = input_grid[i,j]

            # must be bottom
            else:
              for i in range(num_rows_changed):
                for j in range(cols):
                  if input_grid[rows - num_rows_changed + i,j] in swaps:
                    output_grid[i,j] = swaps[input_grid[rows - num_rows_changed + i, j]]
                  else:
                    output_grid[i,j] = input_grid[rows- num_rows_changed + i,j]

            return True

        return False


    # Determine mirroring type (columns or rows) and apply transformation
    if not mirror_columns(input_grid, output_grid):
        mirror_rows(input_grid, output_grid)

    return output_grid.tolist()