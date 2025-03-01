"""
1. Preserve Existing Colors: Copy all pixels from the input grid to the output grid, except for pixels with color 0 (white).
2. Fill with Pattern: For all the white (0) pixels, replace with a repeating horizontal pattern of six 2's followed by three 3's, starting from the top-left corner. The pattern continues across the entire grid, row by row, overwriting only white pixels. The other colors are unaffected.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # define the pattern
    pattern = [2, 2, 2, 2, 2, 2, 3, 3, 3]
    pattern_length = len(pattern)

    # change output pixels 
    for r in range(rows):
        for c in range(cols):
            # only fill if current pixel is white (0)
            if output_grid[r, c] == 0:
               pattern_index = ( (r * cols + c) % pattern_length )
               output_grid[r,c] = pattern[pattern_index]

    return output_grid