"""
The transformation rule is: Iterate through all gray (5) pixels in the input grid.
If a gray pixel has another gray pixel immediately to its right, change the right-side gray pixel to white (0).
Essentially, this removes the right-most gray pixels of any horizontal two-or-more sequence of gray pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current pixel is gray (5)
            if input_grid[i][j] == 5:
                # Check if there's a pixel to the right and if it's also gray
                if j + 1 < cols and input_grid[i][j + 1] == 5:
                    # Change the right side gray pixel to white (0)
                    output_grid[i][j+1] = 0

    return output_grid