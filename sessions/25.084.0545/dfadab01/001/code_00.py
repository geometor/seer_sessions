"""
1.  **Mirror:** Create output grid that is the mirror of the input grid using the anti-diagonal as mirror axis.
2.  **Recolor based on original input:** Iterate through each pixel of the *original input* grid, and based on the color found at coordinates `(r,c)` update color value in *output* grid in position `(c,r)`. Recoloring works as follows:

    *   If the input pixel is red (2), the output pixel in the mirrored position becomes yellow (4).
    *   If the input pixel is green (3), the output pixel in the mirrored position becomes blue (1).
    *   If the input pixel is grey (5), the output pixel in the mirrored position becomes magenta (6).
    *   If the input pixel is magenta (6), the output pixel in the mirrored position becomes white (0).
    *   Other colors in the input grid, including white (0), remain unchanged in the output grid (copied directly after mirroring).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)

    # Mirror and Recolor
    for r in range(rows):
        for c in range(cols):
            output_grid[c, r] = input_grid[r, c]  # Mirror
            if input_grid[r, c] == 2:
                output_grid[c, r] = 4
            elif input_grid[r, c] == 3:
                output_grid[c, r] = 1
            elif input_grid[r, c] == 5:
                output_grid[c, r] = 6
            elif input_grid[r,c] == 6:
                output_grid[c,r] = 0

    return output_grid.tolist()