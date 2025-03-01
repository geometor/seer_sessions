"""
The transformation fills contiguous horizontal runs of white pixels with green, row by row. The fill operation in a given row is interrupted by red pixels. If a row starts with a white pixel and is filled with green and there are no interrupting red pixels, the fill extends to the end of the row.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        filling = False
        blocked = False
        for c in range(cols):
            # Start filling if we encounter a white pixel
            if output_grid[r, c] == 0 and not filling:
                filling = True
                output_grid[r,c] = 3
            # If filling and see red, stop filling, and set blocked flag.
            elif filling and output_grid[r,c] == 2:
                filling = False
                blocked = True
            # fill
            elif filling and output_grid[r,c] == 0:
                output_grid[r,c] = 3

        # extend fill to right of image if row started with 3 AND not blocked
        if output_grid[r, 0] == 3 and not blocked:
            for c in range(cols):
                if output_grid[r,c] != 2:
                    output_grid[r, c] = 3
                else:
                    break  # stop extending at red pixel

    return output_grid