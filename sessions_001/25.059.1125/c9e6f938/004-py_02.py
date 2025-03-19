"""
Duplicate the input grid horizontally. In the duplicated section, extend any orange (7) pixels to fill the space to the right until reaching a white (0) pixel or the grid edge.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid by horizontally concatenating the input grid with itself.
    output_grid = np.concatenate((input_grid, input_grid), axis=1)

    rows, cols = input_grid.shape
    
    # Iterate through the right half of the output_grid (the duplicated part).
    for i in range(rows):
        for j in range(cols, 2 * cols):
            # Check if there is a orange pixel in the corresponding position on left
            if output_grid[i,j-cols] == 7:
               if i + 1 < rows:
                    output_grid[i+1,j]=7

    return output_grid