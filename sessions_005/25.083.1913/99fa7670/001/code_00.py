"""
Iterates through each non-zero pixel in the input grid. For each:
    a. Extends Horizontally: Changes pixels to the right (same row) to match the original pixel's color.
    b. Extends Vertically: Changes pixels below (same column) to match the original pixel's color.
Returns the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:
                # Extend Horizontally
                for k in range(j + 1, cols):
                    if output_grid[i][k] == 0:
                        output_grid[i][k] = input_grid[i][j]
                    else:
                        break #stop when different value is found

                # Extend Vertically
                for k in range(i + 1, rows):
                    if output_grid[k][j] == 0:
                        output_grid[k][j] = input_grid[i][j]
                    else:
                        break #stop when different value is found
    return output_grid