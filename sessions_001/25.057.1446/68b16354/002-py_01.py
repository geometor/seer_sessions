"""
The transformation rule is to reflect the input grid vertically across its horizontal midline. This is equivalent to reversing the order of the rows.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a numpy array
    output_grid = np.array(input_grid)
    
    # reverse the order of rows.
    output_grid = np.flipud(output_grid)

    return output_grid.tolist() # convert back to python list