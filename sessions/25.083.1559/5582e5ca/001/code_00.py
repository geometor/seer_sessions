"""
1.  **Inspect the input grid:** Examine all the pixel color values within the input grid.
2.  **Determine the output color:** select the top left corner pixel of the input grid.
3.  **Create the output grid:**
    *   Create a new grid with the same dimensions (width and height) as the input grid.
    *   Fill every cell of the output grid with the color found in the previous step.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as input_grid
    output_grid = np.zeros_like(input_grid)

    # get the color of the top-left pixel in the input grid
    output_color = input_grid[0, 0]

    # fill the output grid with this color
    output_grid[:] = output_color

    return output_grid