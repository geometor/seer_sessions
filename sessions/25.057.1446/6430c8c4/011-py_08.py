"""
1.  **Find the Marker:** Locate the blue (1) pixel within the input grid.
2.  **Calculate Output Dimensions** Count the total number of columns to the right of the blue pixel, inclusive, Call this count `c`. The output grid is a square with dimensions `c` x `c`
3.  **Create Output Grid:** Initialize an output grid of the calculated dimensions, filled entirely with white (0) pixels.
4.  **Place Corner Markers:** Set the pixel values at the four corners of the output grid to green (3):
    *   Top-left: (0, 0)
    *   Top-right: (0, c-1)
    *   Bottom-left: (c-1, 0)
    *   Bottom-right: (c-1, c-1)
5. return the output grid
"""

import numpy as np

def transform(input_grid):
    # Find the blue (1) pixel.  Assume there's only one.
    def find_blue_pixel(grid):
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 1:
                    return (r, c)
        return None  # Should not happen in these examples

    blue_pixel_location = find_blue_pixel(input_grid)

    # Calculate output dimensions.
    c = input_grid.shape[1] - blue_pixel_location[1]

    # Create output grid filled with white (0).
    output_grid = np.zeros((c, c), dtype=int)

    # Place green (3) pixels in corners.
    output_grid[0, 0] = 3
    output_grid[0, -1] = 3
    output_grid[-1, 0] = 3
    output_grid[-1, -1] = 3

    return output_grid