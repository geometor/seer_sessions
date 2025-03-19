"""
The output grid's dimensions are determined by removing columns containing a specific color (determined per example) from the input grid. If blue is present, remove all columns that contain blue. Otherwise, if there is only one color in the whole image, no columns are removed. If any other condition is true, remove all columns that have white. Then compress the remaining columns. If a cell had a blue above or to the left it is set to green. Otherwise, the color is unchanged.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Determine which color to check for column removal
    if 1 in input_grid:
        color_to_remove = 1  # Blue
    elif len(np.unique(input_grid)) == 1:
        color_to_remove = None #no colors removed
    else:
        color_to_remove = 0 # White

    # Find columns that contain the color to remove
    if color_to_remove is not None:
      cols_to_keep = [i for i in range(cols) if color_to_remove not in input_grid[:, i]]
    else:
      cols_to_keep = [i for i in range(cols)] # keep all cols.


    # Create a new grid with only the selected columns
    temp_grid = input_grid[:, cols_to_keep]

    output_rows, output_cols = temp_grid.shape
    output_grid = temp_grid.copy()

    # Iterate through the new grid and apply the green color rule
    for r in range(output_rows):
        for c in range(output_cols):
            if (r > 0 and temp_grid[r-1, c] == 1) or (c > 0 and temp_grid[r, c-1] == 1):
                output_grid[r, c] = 3  # Green

    return output_grid.tolist()