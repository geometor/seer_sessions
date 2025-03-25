"""
Iterate through each pixel of the input grid.
If the pixel's color is 6 (magenta), change it to 2 (red) in the output grid.
Otherwise, keep the pixel's color unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing pixels of color 6 to color 2.
    Other colors remain unchanged.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy to avoid modifying the original

    # Iterate through rows and columns of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check pixel color and change if necessary
            if output_grid[i, j] == 6:
                output_grid[i, j] = 2
            #Implicit else, leave color the same

    return output_grid