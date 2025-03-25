"""
The transformation rule takes the input grid and mirrors it horizontally. The
output grid has the same number of rows as the input grid, but twice the number
of columns. The left half of the output grid is identical to the input grid.
The right half of the output grid is a mirrored image of the input grid,
flipped along the vertical axis.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Get dimensions of the input grid
    rows, cols = input_array.shape

    # Create output grid by mirroring horizontally
    output_array = np.concatenate((input_array, np.fliplr(input_array)), axis=1)
    
    return output_array.tolist()