"""
The transformation rule is as follows:

1.  The input is a single row of pixels (1 x N).
2.  The output is a 15x15 grid.
3.  Place the input row along the anti-diagonal of the output grid, starting from the bottom-left corner (14,0).
4.  Fill all remaining cells of the output grid with black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 15x15 array filled with 0s.
    output_grid = np.zeros((15, 15), dtype=int)

    # Get the input row.
    input_row = input_grid[0]
    input_len = len(input_row)

    # Place the input row on the anti-diagonal.
    for i in range(input_len):
        output_grid[14 - i, i] = input_row[i]

    return output_grid