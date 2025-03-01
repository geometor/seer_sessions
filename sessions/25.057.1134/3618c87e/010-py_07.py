"""
The transformation rule swaps the positions of the single, isolated blue (1) and gray (5) pixels in the input grid.  If there are multiple blue or grey pixels, or no pixels of a given color, it doesn't apply. It only swaps a *single* blue pixel with a *single* grey pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all blue (1) pixels.
    blue_coords = np.argwhere(input_grid == 1)

    # Find the coordinates of all gray (5) pixels.
    gray_coords = np.argwhere(input_grid == 5)

    # Swap colors only if there's exactly one blue and one gray pixel
    if len(blue_coords) == 1 and len(gray_coords) == 1:
        blue_coord = blue_coords[0]
        gray_coord = gray_coords[0]
        output_grid[blue_coord[0], blue_coord[1]] = 5
        output_grid[gray_coord[0], gray_coord[1]] = 1

    return output_grid