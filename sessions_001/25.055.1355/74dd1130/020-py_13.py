"""
The transformation involves transposing the input grid. Specifically, the rows of the input grid become the columns of the output grid, and vice versa.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as numpy array for easier transposing
    output_grid = np.array(input_grid)

    # transpose the grid
    output_grid = output_grid.T
    
    #convert back to python list
    output_grid = output_grid.tolist()

    return output_grid