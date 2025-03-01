"""
The input grid is duplicated horizontally. Orange regions, identified in the original half of the grid, are extended to the right in the mirrored positions within the duplicated half. The extension continues until a pixel that is not orange or the right edge of the duplicated grid is encountered.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid by horizontally concatenating the input grid with itself.
    output_grid = np.concatenate((input_grid, input_grid), axis=1)

    rows, cols = input_grid.shape

    # Iterate through the original (left) half of the grid.
    for i in range(rows):
        for j in range(cols):
            # Check for orange pixels in the original half.
            if input_grid[i, j] == 7:
                # Extend orange in the duplicated (right) half.
                for k in range(cols + j, 2 * cols):
                    if output_grid[i, k - cols] != 7 :
                        break #stop at non-orange
                    if k < 2 * cols:
                        output_grid[i, k] = 7
                    else:
                        break #stop at edge


    return output_grid