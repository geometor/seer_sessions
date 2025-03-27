"""
The transformation rule is as follows:

1.  **Preserve the Border:** The outermost rows and columns of the grid remain identical in the input and output.
2.  **Interior Transformation:** For cells not on the border:
    *   Examine horizontal runs of digits. Vertical runs do *not* appear to matter.
    *   Runs of length 6 or greater are modified.
    *   The color '2' is never modified.
    *   Within a modifiable run, it's every other pixel starting with the second pixel in the run.
    *   The replacement color is the color of the run itself.

"""

import numpy as np

def get_horizontal_runs(grid):
    """
    Identifies horizontal runs of identical digits within the grid.
    Returns a list of runs, where each run is a list of (row, col) tuples.
    """
    rows = len(grid)
    cols = len(grid[0])
    runs = []
    for r in range(rows):
        current_run = []
        for c in range(cols):
            if len(current_run) == 0:
                current_run.append((r, c))
            elif grid[r][c] == grid[r][current_run[-1][1]]:
                current_run.append((r, c))
            else:
                runs.append(current_run)
                current_run = [(r, c)]
        if len(current_run)>0:
            runs.append(current_run)
    return runs

def transform(input_grid):
    # initialize output_grid
    output_grid = [row[:] for row in input_grid] # deep copy
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Get all horizontal runs
    runs = get_horizontal_runs(input_grid)

    # change output pixels based on the runs
    for run in runs:
        first_pixel_row, first_pixel_col = run[0]
        color = input_grid[first_pixel_row][first_pixel_col]
        
        if color != 2:  # Don't modify runs of color 2
          if len(run) >= 6: #train 1 and train 2
            for i in range(1,len(run), 2): # alternate every other element of the run, starting with the *second*
              output_grid[run[i][0]][run[i][1]] = color


    return output_grid