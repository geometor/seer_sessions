"""
1.  Identify: Find all pixels with the color yellow (value 4) in the input grid.
2.  Reposition Vertically: In the output grid, place yellow pixels in the first column (column index 0) in every row from 0 up to and including 5, as well as row 7.
3.  Reposition Horizontally: Place yellow pixels in the seventh row (row index 6) across every column.
4.  Clear Other: All other pixels in the output grid should be set to black (or the background color, which is 0 in this case).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Reposition Vertically: Place yellow pixels in the first column (index 0)
    for r in range(rows):
        if r <= 5 or r == 7:
            output_grid[r, 0] = 4

    # Reposition Horizontally: Place yellow pixels in the seventh row (index 6)
    for c in range(cols):
        output_grid[6, c] = 4


    return output_grid