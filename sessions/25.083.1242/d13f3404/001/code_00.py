"""
The transformation rule takes an input grid and replicates its pattern diagonally downwards and to the right. The output grid's dimensions are determined by adding the number of rows and columns of the input grid and subtracting 1.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows + input_cols - 1
    output_cols = output_rows
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # change output pixels 
    for i in range(input_rows):
        for j in range(input_cols):
            for k in range(output_rows - max(i,j)):
              if i + k < output_rows and j + k < output_cols:
                output_grid[i + k, j + k] = input_grid[i, j]

    return output_grid