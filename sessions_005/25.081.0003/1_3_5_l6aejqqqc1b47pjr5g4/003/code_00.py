"""
The transformation rule is a "waterfall" effect where yellow pixels (4) propagate downwards in each column. The propagation stops either at the bottom edge of the grid or one row below a row containing any yellow pixel. Propagation is column-specific.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the waterfall rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Column-wise Iteration
    for col in range(cols):
        # Yellow Pixel Check (within the column)
        has_yellow = False
        for row in range(rows):
          if input_grid[row,col] == 4:
            has_yellow = True

        if has_yellow:
            # Propagation
            last_yellow_row = -1
            for row in range(rows):
                if 4 in input_grid[row,:]: # check if the whole row has any yellow.
                    last_yellow_row = row

            for row in range(rows):
               if row <= last_yellow_row + 1: # Check the condition for the waterfall effect.
                    if input_grid[row,col] == 4:  # propogate self
                        output_grid[row, col] = 4

                        if row+1<rows:   # propagate one down
                            output_grid[row+1,col]=4


    return output_grid.tolist()