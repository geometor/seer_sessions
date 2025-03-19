"""
The output grid is created by selecting the leftmost section of the input grid, up to the fourth column (index 3 inclusive).
"""

import numpy as np

def transform(input_grid):
    """
    Selects a subgrid from the input grid to form the output grid.
    """
    # Initialize the output grid based on input dimensions.  We'll trim it later.
    input_grid = np.array(input_grid) # ensure numpy array
    output_grid = input_grid.copy()

    # Select the subgrid:  all rows, columns from 0 up to (and including) 3.
    output_grid = output_grid[:, 0:4]

    return output_grid.tolist() # return as list
