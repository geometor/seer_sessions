"""
Transforms the input grid based on color-specific rules, primarily focusing on horizontal adjacency and runs of colors.
Changes colors based on the neighbors in specific rows.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a series of color transformations to the input grid based on neighbor colors
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check First Row changes:
            if r == 0:
                # If color 6 and right neighbor is color 3, change color to 3.
                if input_grid[r, c] == 6 and c + 1 < cols and input_grid[r, c+1] == 3:
                    output_grid[r, c] = 3
                # If color 3 and left neighbor is color 7, change color to 7.
                elif input_grid[r, c] == 3 and c - 1 >= 0 and input_grid[r, c-1] == 7:
                    output_grid[r, c] = 7
            # Check other row changes based on the row above
            else:
                # If color is 6 and above neighbor is 6, change to color of cell directly above.
                if input_grid[r,c] == 6 and input_grid[r-1, c] == 6:
                    output_grid[r,c] = input_grid[r-1,c]
                # specific row change
                if input_grid[r,c] == 1:
                    # check for 7 in same row to change to 1.
                    for c2 in range(cols):
                        if output_grid[r,c2] == 7:
                            output_grid[r,c2] = 1
    return output_grid