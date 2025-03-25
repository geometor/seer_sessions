"""
Transforms input grids to output grids based on the position of gray (5) pixels and row sections.
Specifically:
1.  **Identify Key Rows:** Locate rows that are entirely filled with gray (5) pixels.
2.  **Top Section Transformation:** Above the first all-gray row, change contiguous black (0) pixels to blue (1).
3.  **Middle Section Transformation:** Between the first and second all-gray rows, change contiguous black (0) pixels to red (2).
4.  **Bottom Section Transformation:** Below the second all-gray row, change contiguous black (0) pixels to green (3).
5.  **Preserve Gray Pixels:** All gray (5) pixels remain unchanged.
"""

import numpy as np

def find_all_gray_rows(grid):
    """Finds rows that are entirely filled with gray (5) pixels."""
    gray_rows = []
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            gray_rows.append(i)
    return gray_rows

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    all_gray_rows = find_all_gray_rows(input_grid)
    
    first_group_cols = []
    second_group_cols = []
    third_group_cols = []

    if len(all_gray_rows) >= 1:
        # Top section transformation
        
        # find first group columns
        
        i = 0
        while i < cols:
          if input_grid[0,i] == 0:
            j=i
            while j < cols and input_grid[0,j] == 0 :
              first_group_cols.append(j)
              j+=1
            i = j
          else:
              i += 1

        for r in range(0, all_gray_rows[0]):
            for c in first_group_cols:
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 1

    if len(all_gray_rows) >= 1:

        # find second group columns
        i = 0
        if len(all_gray_rows) > 1:
            reference_row = all_gray_rows[0]+1
        else:
            reference_row = all_gray_rows[0]

        while i < cols:
          if input_grid[reference_row,i] == 0:
            j=i
            while j < cols and input_grid[reference_row,j] == 0 :
              second_group_cols.append(j)
              j+=1
            i = j
          else:
              i += 1

    if len(all_gray_rows) >= 1:
        # Middle section transformation
        if len(all_gray_rows) > 1:
          start_row = all_gray_rows[0] + 1
          end_row = all_gray_rows[1]
        else:
          start_row = all_gray_rows[0] +1
          end_row = rows

        for r in range(start_row, end_row):
             for c in second_group_cols:
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 2

    if len(all_gray_rows) >= 2:

        # find third group columns
        i = 0
        while i < cols:
          if input_grid[all_gray_rows[1]+1,i] == 0:
            j=i
            while j < cols and input_grid[all_gray_rows[1]+1,j] == 0 :
              third_group_cols.append(j)
              j+=1
            i = j
          else:
              i += 1


        # Bottom section transformation
        for r in range(all_gray_rows[1] + 1, rows):
            for c in third_group_cols:
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 3

    return output_grid.tolist()