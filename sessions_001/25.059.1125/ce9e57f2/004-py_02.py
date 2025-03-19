"""
1.  **Identify:** Find all pixels with the color red (value 2).
2.  **Conditional Change**: Starting from the bottom row, examine the existing red vertical pattern. If a red pixel is on or below row 5, it will change to azure.
3.  **Transform:** Change the color of the red pixels in rows 5, 6, and 7, to azure (value 8). All other pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]

    # change output pixels 
    for r in range(rows):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] == 2 and r >= 4 :  # Check for red and row number (starting to count at zero)
                output_grid[r, c] = 8

    return output_grid