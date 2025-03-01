"""
1.  **Initialization:** Create an output grid that is the exact same dimensions as the input grid.

2.  **Border:** Fill the outermost border of the output grid with yellow (4) pixels.

3.  **Inner Pixels:** Iterate through all pixels inside the border (not part of the border) of the *input* grid. If a pixel is not white (0), copy it to the same position in the output grid, changing the pixel to yellow (4). If it *is* zero/white, then fill the cell in the output with white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # Fill border with yellow
            if (r == 0 or r == input_grid.shape[0] - 1 or
                c == 0 or c == input_grid.shape[1] - 1):
                output_grid[r, c] = 4
            elif input_grid[r,c] != 0:
                output_grid[r,c] = 4

    return output_grid.tolist()