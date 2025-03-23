"""
The transformation rule involves swapping elements between the rows and columns.
Each row of the input becomes a column on the output, and conversely each
column of the input becomes a row of the output.
Specifically:
- Input Row 1 becomes Output Column 3
- Input Row 2 becomes Output Column 1
- Input Row 3 becomes Output Column 2
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.empty_like(input_grid)

    # change output pixels
    # Input Row 1 becomes Output Column 3
    output_grid[:, 2] = input_grid[0, :]
    # Input Row 2 becomes Output Column 1
    output_grid[:, 0] = input_grid[1, :]
    # Input Row 3 becomes Output Column 2
    output_grid[:, 1] = input_grid[2, :]

    return output_grid.tolist()