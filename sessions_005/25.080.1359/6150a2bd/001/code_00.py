"""
The input grid is transposed, then the rows are reversed to form the output.
"""

import numpy as np

def transform(input_grid):
    # Transpose the input grid
    transposed_grid = np.transpose(input_grid)

    # Reverse the rows of the transposed grid
    output_grid = np.flip(transposed_grid, axis=0)

    return output_grid