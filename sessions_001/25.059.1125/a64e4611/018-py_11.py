"""
The transformation fills contiguous horizontal runs of white pixels with green, row by row. The fill operation in a given row is interrupted by red pixels. If a row starts with a white pixel, filling begins immediately. Filling continues until a red pixel is encountered or the end of the row is reached.  If a red pixel is encountered, filling stops for that segment, but can restart if another white pixel is found later in the same row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        filling = False
        for c in range(cols):
            # Start filling if we encounter a white pixel and we are not already filling
            if output_grid[r, c] == 0 and not filling:
                filling = True
                output_grid[r, c] = 3  # Fill with green
            # If filling and see red, stop filling.
            elif filling and output_grid[r, c] == 2:
                filling = False
            # Continue filling with green if currently filling and the pixel is white
            elif filling and output_grid[r, c] == 0:
                output_grid[r, c] = 3  # Fill with green

    return output_grid