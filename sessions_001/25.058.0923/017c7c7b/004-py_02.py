"""
Iterate through each pixel of the input grid.
If a pixel is blue (1), change it to red (2) in the output grid.
If a pixel is white (0), keep it white (0) in the output grid.
If a pixel is another color, keep it the same in the output grid.
Add one new row to the bottom of the output grid. The values of this row may change based on patterns seen in the other values of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with one extra row
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows + 1, input_cols), dtype=int)

    # Change blue pixels to red, keep white and other pixels the same
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 1:
                output_grid[i, j] = 2
            else:
                output_grid[i, j] = input_grid[i,j]

    # Add a new row at the bottom.  Fill with a simple pattern for now.
    # Need to refine this logic later.
    for j in range(input_cols):
        if j < input_cols -1:
            output_grid[input_rows, j] = 0
        else:
            output_grid[input_rows,j] = 2


    return output_grid