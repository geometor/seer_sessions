"""
The transformation extracts the first two columns of the input grid if the input grid has more than 2 columns. Otherwise, it returns the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Get number of columns
    cols = input_grid.shape[1]

    # Extract first two columns if input has more than 2 columns
    if cols > 2:
        output_grid = input_grid[:, :2]
    else:
        output_grid = input_grid

    return output_grid.tolist()