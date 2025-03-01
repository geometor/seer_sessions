"""
The transformation preserves the existing azure (8) pixels and selectively introduces blue (1) pixels in the locations that follow the perceived checkerboard pattern established in the top section of the grid. The output shows the bottom part of the pattern being completed with color '1'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling in missing azure (8) pixels in the checkerboard
    pattern with blue (1) pixels, starting from row 6.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid starting from row 6
    for r in range(5, rows):
        for c in range(cols):
            # Check for the expected checkerboard pattern
            # Azure should be present based on position on grid.
            # start a pattern, then skip a line. start a pattern, then skip a line.
            
            if (r-1) % 2 == 0 and c % 2 == 1:
                if output_grid[r,c] == 0:
                    output_grid[r,c] = 1

            elif (r) % 2 == 0 and c % 2 == 0:
                if output_grid[r,c] == 0:
                    output_grid[r,c] = 1

    return output_grid