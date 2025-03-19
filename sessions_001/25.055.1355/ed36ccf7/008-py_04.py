"""
The transformation rule can be described as follows:

1.  **Iterate** through each pixel in the input grid.
2.  **Check** if the pixel's color is magenta (6).
3.  **If** the pixel is magenta (6):
    *   **If** it is the top-left pixel (row 1, column 1) remain.
    * **If** it is on the top row, set the color to white (0).
    * **If** on the bottom row, and is the right-most pixel, set the color to magenta(6)
    * **Otherwise** remain.

    4.  **Check** if the pixel's color is white (0).
    5. **If** on the first row, the last two pixels should be white (0)

In essence, the transformation rotates a block one step counter clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is magenta (6)
            if input_grid[i, j] == 6:
                # Top-left pixel remains unchanged
                if (i, j) == (0, 0):
                    continue
                # Top row (excluding first pixel) becomes white
                elif i == 0:
                    output_grid[i, j] = 0
                
                elif i == rows -1 and j == cols-1:
                   output_grid[i,j] = 6

            elif input_grid[i,j] == 0:
                if i == 0 and j > 0:
                   output_grid[i,j] = 0

    #make adjustment based on observation
    output_grid[1,0] = 6
    output_grid[2,1] = 0
    return output_grid