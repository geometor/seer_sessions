"""
The transformation takes each row of the input grid and expands it horizontally in the output grid. 
The output grid is twice as wide as the input grid.
For each row, the transformation duplicates any sequence of 7s (orange pixels) horizontally,
maintaining the relative positions of 0s (white pixels). The number of 0's before and after the
sequence of 7's are determined by their relative position in the input.
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
        
        # Count 7's before this position
        count_7 = 0

        # Iterate through the input row
        for i in range(len(row)):
           if row[i] == 7:
              count_7 +=1
        
        for i in range(len(row)):
           if row[i] == 7:
               output_row.append(7)
               output_row.append(7)
           else:
               output_row.append(0)

        # put the row values starting at an offset of count_7 * 0
        output_grid[row_index, :len(output_row)] = output_row

    return output_grid