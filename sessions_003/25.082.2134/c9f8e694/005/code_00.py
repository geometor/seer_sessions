"""
Iterate through the grid. If a pixel has a non-zero left neighbor and there are only zeros between the current pixel and any previous non-zero pixels of a different color, change the current pixel's color to the left neighbor's color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on left neighbor color propagation with zero separation.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for row in range(rows):
        for col in range(cols):
            # Check left neighbor
            if col > 0:
                left_neighbor = output_grid[row, col - 1]
                if left_neighbor != 0 :
                    # Check for zero separation and different color
                    propagate = True
                    for i in range(col - 1):
                         if output_grid[row,i] != 0 and output_grid[row,i] != left_neighbor:
                              propagate = False
                              break

                    if propagate and output_grid[row, col] != left_neighbor and output_grid[row,col] != 0:
                        output_grid[row, col] = left_neighbor

    return output_grid