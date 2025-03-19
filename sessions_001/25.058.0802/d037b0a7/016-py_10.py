"""
Copy the second row of the input grid to the third row of the output grid.
The first and second rows of the output grid are different than those of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This is a good practice,
    # even if we end up overwriting all the rows later.
    output_grid = np.copy(input_grid)

    # Get the number of rows in the input grid
    num_rows = input_grid.shape[0]

    # Check if the input grid has at least 2 rows
    if num_rows >= 2:
        # Copy the second row to the third row, if the output grid has a third row.
        if num_rows >= 3:
          output_grid[2, :] = input_grid[1, :]
        
        # make all the rows the second row
        output_grid[0, :] = input_grid[1, :]
        output_grid[1, :] = input_grid[1, :]


    return output_grid