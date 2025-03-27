"""
Transforms the input grid based on color-specific rules, primarily focusing on horizontal runs of color 6 and specific color propagations.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a series of color transformations to the input grid based on horizontal runs and propagations
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to find horizontal runs
    def find_horizontal_runs(grid, color):
        runs = []
        for r in range(rows):
            in_run = False
            start_col = 0
            for c in range(cols):
                if grid[r, c] == color:
                    if not in_run:
                        in_run = True
                        start_col = c
                elif in_run:
                    in_run = False
                    runs.append((r, start_col, c - 1))
            if in_run:
                runs.append((r, start_col, cols - 1))
        return runs

    # 1. Color 6 Replacement
    runs_of_6 = find_horizontal_runs(output_grid, 6)
    for r, start_c, end_c in runs_of_6:
        if r == 0:
            # Change all 6s in row 0 to 3
            for c in range(start_c, end_c + 1):
                output_grid[r, c] = 3
        elif r in (2, 3, 4) and end_c - start_c + 1 >= 2:
            # Change runs of two or more 6s in rows 2, 3, and 4 to 4
             for c in range(start_c, end_c+1):
                output_grid[r,c] = 4
        elif r in (4,5) and end_c - start_c + 1 >= 2:
            for c in range(start_c, end_c+1):
                output_grid[r,c] = 1


    # 2. Color Propagation (3 to 7)
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 3:
          if r == 0:
            if c >= 2 and input_grid[r, c-1] == 6 and input_grid[r,c-2] == 6:
               output_grid[r,c] = 7
          elif r == 1:
            output_grid[r,c] = 7

    return output_grid