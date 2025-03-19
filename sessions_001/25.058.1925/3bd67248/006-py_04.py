"""
1. Determine Output Grid Height: The output grid's height is either equal to the input grid's height or one less.
2. Remove Magenta: Remove all magenta (6) pixels from the input.
3. Create Red Diagonal: Create a diagonal line of red (2) pixels. The line starts at the top-right corner of the *output* grid.  It extends diagonally down and to the left, one cell at a time. The length appears to be governed by the height.
4. Fill Below Red with Yellow: Fill all cells directly below the red (2) pixels with yellow (4) pixels, extending to the bottom of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Grid Height: The output grid's height is either equal to the input grid's height or one less.
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows if input_rows <= input_cols else input_rows -1
    output_cols = input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # copy input to output, removing magenta
    for r in range(input_rows):
        for c in range(input_cols):
            if r < output_rows: # ensure we do not write beyond output grid
                if input_grid[r,c] != 6:
                    output_grid[r,c] = input_grid[r,c]

    # Create Red Diagonal: Create a diagonal line of red (2) pixels, starting from top-right corner of output grid.
    for i in range(min(output_rows, output_cols)):
        output_grid[i, output_cols - 1 - i] = 2

    # Fill Below Red with Yellow: Fill cells below the red pixels with yellow (4).
    for r in range(output_rows):
        for c in range(output_cols):
            if output_grid[r, c] == 2:
                for r_below in range(r + 1, output_rows):
                    output_grid[r_below, c] = 4
    return output_grid