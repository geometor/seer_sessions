"""
The transformation rule is as follows:
1. Identify the Key Colors: Find all cells that are not white (0).
2. Propagation of the Dominant color, magenta (6): Iterate to fill all cells that are white to magenta if the cell to its right is magenta.
3. Fill with the Center Color: All the remaining white cells (0) will be the same color of the center cell, yellow (4).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center color
    center_color = output_grid[rows // 2, cols // 2]

    # Iterate through the grid
    for i in range(rows):
        for j in range(cols):
            # Propagation of magenta (6)
            if j < cols - 1 and output_grid[i, j+1] == 6:
                if output_grid[i,j] == 0:
                    output_grid[i, j] = 6
            # Fill remaining 0s with the center color
            elif output_grid[i,j] == 0:
                output_grid[i,j] = center_color


    return output_grid