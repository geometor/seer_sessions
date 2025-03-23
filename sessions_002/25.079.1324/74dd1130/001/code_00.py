"""
The transformation performs a cyclic permutation of the input columns, placing the original second column in the first output columns position, the original third column in the second output column position, and the original first column in the third output column position.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.empty_like(input_grid)

    # change output pixels
    # The second column in input becomes the first column in output.
    output_grid[:, 0] = input_grid[:, 1]
    #  The third column of input, becomes second column of output
    output_grid[:, 1] = input_grid[:, 2]
    # The first column in input becomes last column in output.
    output_grid[:, 2] = input_grid[:, 0]


    return output_grid.tolist()