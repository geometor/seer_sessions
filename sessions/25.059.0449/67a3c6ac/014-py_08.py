"""
The transformation rule is a 180-degree rotation of the entire input grid. This can be visualized as follows:

1.  **Identify the Center:** Determine the center point of the grid. For grids with odd dimensions (e.g., 3x3, 5x5), this is the exact middle pixel. For grids with even dimensions, the center is conceptually between the central pixels.

2.  **Rotate 180 Degrees:** Imagine rotating the entire grid by 180 degrees around this center point. Each pixel in the input grid will have a corresponding new position in the output grid.

3. **Pixel Mapping Formula:** The new position of a pixel can be calculated directly. A pixel located at `(row, col)` in the input grid moves to `(total_rows - 1 - row, total_cols - 1 - col)` in the output grid. This effectively performs both a horizontal and a vertical reflection, resulting in the 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # get dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # calculate the mirrored indices for 180-degree rotation
            mirrored_i = rows - 1 - i
            mirrored_j = cols - 1 - j

            # assign pixel value from input to corresponding mirrored position in output
            output_grid[mirrored_i, mirrored_j] = input_grid[i, j]

    return output_grid