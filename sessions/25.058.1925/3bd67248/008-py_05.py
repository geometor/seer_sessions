"""
1. Remove Magenta: Remove all magenta (6) pixels from the input grid.
2. Determine Output Grid Height: The output grid's height is the same as the input grid's height.
3. Determine Output Grid Width: The output grid's width is the same as the input grid's width.
4. Create Red Diagonal: Create a diagonal line of red (2) pixels. The line starts at the top-right corner of the output grid. It extends diagonally down and to the left. The length of the diagonal is equal to the height of the input grid.
5. Fill Below Red with Yellow: Fill all cells directly below the red (2) pixels with yellow (4) pixels, extending to the bottom of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Grid Height and Width: The output grid's dimensions are the same as the input.
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows
    output_cols = input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # copy input to output, removing magenta
    for r in range(input_rows):
        for c in range(input_cols):
            if input_grid[r,c] != 6:
                output_grid[r,c] = input_grid[r,c]

    # Create Red Diagonal: Create a diagonal line of red (2) pixels.
    # The length of the diagonal is equal to the height (number of rows) of the *input* grid.
    for i in range(output_rows):
        output_grid[i, output_cols - 1 - i] = 2

    # Fill Below Red with Yellow: Fill cells below the red pixels with yellow (4).
    for r in range(output_rows):
        for c in range(output_cols):
            if output_grid[r, c] == 2:
                for r_below in range(r + 1, output_rows):
                    output_grid[r_below, c] = 4

    return output_grid