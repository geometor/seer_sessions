"""
Expands the input grid horizontally by a factor of 2. 
Each original column is copied to the output, and 
a column of 0s is inserted after each copied column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with double the width, filled with 0s.
    input_grid = np.array(input_grid)
    output_width = input_grid.shape[1] * 2
    output_height = input_grid.shape[0]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input columns and copy them to the output grid.
    for i in range(input_grid.shape[1]):
        output_grid[:, 2 * i] = input_grid[:, i]

    # Columns of 0s are already present due to initialization.

    return output_grid.tolist()