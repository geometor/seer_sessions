"""
The transformation fills contiguous horizontal runs of white pixels with green, row by row, starting from the top-left. The fill operation in a given row is either interrupted by existing red pixels, or fills a gap between them completely. Then fill extends to the end of rows.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        filling = False
        for c in range(cols):
            # Start filling if we encounter a white pixel and are not already filling
            if output_grid[r, c] == 0 and not filling:
                filling = True
                output_grid[r,c] = 3
            # If filling and see red, stop filling for this gap.
            elif filling and output_grid[r,c] == 2:
              filling = False
            # fill
            elif filling and output_grid[r,c] == 0:
                output_grid[r,c] = 3

        # extend fill to right of image if row starts with 3
        if output_grid[r,0] == 3:
            for c in range(cols):
                output_grid[r,c] = 3


    return output_grid