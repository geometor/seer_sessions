"""
Transforms a 3x3 input grid into a 5x3 output grid based on column-wise rules.
The first element of each input column is replicated down the entire corresponding output column.
The second element of the input column is placed into the second row of the output column only if
the cell has not been populated by the first element. The rest of the output column is filled with zero.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a 5x3 array filled with zeros.
    output_grid = np.zeros((5, 3), dtype=int)

    # Iterate through each column of the input grid
    for col_index in range(input_grid.shape[1]):
        # Copy the first element of the input column to fill the entire output column.
        output_grid[:, col_index] = input_grid[0, col_index]
        
        # Copy the second element if the corresponding output cell is zero.
        if output_grid[1, col_index] == 0:
           output_grid[1, col_index] = input_grid[1,col_index]

    return output_grid