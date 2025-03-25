```python
"""
Transforms the input grid based on the location and length of horizontal runs of magenta (color 6) pixels.  Specific rows are handled differently.
"""

import numpy as np

def transform(input_grid):
    """
    Applies color transformations based on horizontal magenta runs.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to find horizontal runs of a specific color
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

    # 1. Magenta (6) Runs on Row 0
    runs_of_6 = find_horizontal_runs(output_grid, 6)
    for r, start_c, end_c in runs_of_6:
        if r == 0:
            for c in range(start_c, end_c + 1):
                output_grid[r, c] = 3

    # 2. Magenta Runs in Rows 2, 3, and 4
        elif r in (2, 3, 4) and end_c - start_c + 1 >= 2:
            for c in range(start_c, end_c + 1):
                output_grid[r, c] = 4

    # 3. Magenta runs in rows 4 and 5
        elif r in (4, 5) and end_c - start_c + 1 >= 3:
             for c in range(start_c, end_c + 1):
                output_grid[r,c] = 1

    return output_grid
```