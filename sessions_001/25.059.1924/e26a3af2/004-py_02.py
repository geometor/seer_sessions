"""
The transformation rule is as follows:
1. Identify the columns in the input grid that contain only the colors azure (8), green (3), and red (2).
2. Keep only these identified columns.
3. Replace all colors *not* in the identified columns with blue (1).
4. The output grid consists of the identified columns, maintaining their original dimensions and relative positions, and all other pixels are blue(1).
"""

import numpy as np

def get_columns_of_interest(grid):
    # identify columns of interest - with colors 8, 3, 2
    cols_of_interest = []
    for j in range(grid.shape[1]):
        unique_colors = np.unique(grid[:, j])
        if len(unique_colors) == 1 and unique_colors[0] in [8, 3, 2]:
            cols_of_interest.append(j)
    return cols_of_interest

def transform(input_grid):
    # initialize output_grid as all blue (1)
    output_grid = np.ones_like(input_grid)

    # get columns of interest
    cols_of_interest = get_columns_of_interest(input_grid)

    # place columns of interest into output_grid
    for j in cols_of_interest:
      output_grid[:,j] = input_grid[:,j]

    return output_grid