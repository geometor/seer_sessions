"""
The output grid is identical to the input grid. There is no transformation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.  This isn't strictly necessary
    # for this trivial transformation, but it's good practice as it can
    # make other grid operations easier if the transformation were more complex.
    output_grid = np.array(input_grid)

    # Return the output grid, which is a copy of the input grid.
    return output_grid.tolist()