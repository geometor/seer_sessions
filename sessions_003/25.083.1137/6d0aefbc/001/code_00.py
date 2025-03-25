"""
The transformation rule is to duplicate each column of the input grid, effectively doubling the width of the grid while preserving its height and the order of elements within each original column.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_width = input_grid.shape[1] * 2
    output_height = input_grid.shape[0]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for i in range(input_grid.shape[1]):
        # Copy the column.
        column = input_grid[:, i]
        
        # Insert the original column into the output grid.
        output_grid[:, 2*i] = column
        
        # Immediately insert the copied column adjacent to the original.
        output_grid[:, 2*i + 1] = column

    return output_grid.tolist()