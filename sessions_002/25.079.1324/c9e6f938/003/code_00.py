"""
For each row:

1.  Double the width of the output row.
2.  Iterate through the input row.
3.  Copy each pixel's value to the output row at same position.
4.  Duplicate any orange (7) pixel.
5.  Mirror the entire filled part of the row so the beginning is the same as the end.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with twice the width of the input grid
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows, input_cols * 2), dtype=int)

    # Iterate through each row of the input grid
    for row_index, row in enumerate(input_grid):
        # build output row and use it to fill output_grid
        output_row = []

        # Iterate through the input row and duplicate 7s
        for i in range(len(row)):
           if row[i] == 7:
               output_row.append(7)
               output_row.append(7)
           else:
               output_row.append(row[i])

        # put the row values
        output_grid[row_index, :len(output_row)] = output_row

        # mirror the filled part
        for i in range(len(output_row)):
           output_grid[row_index, output_grid.shape[1]-1-i] = output_grid[row_index,i]
    return output_grid