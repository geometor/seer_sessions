"""
1.  Identify the initial white pixel: Locate the single white pixel (0) in the input grid.
2.  Center Cross: In the output grid, the red pixel at the center of the grid remains.
3.  White Cross: All other red pixels that are on the same row or column of the original white pixel are changed to white pixels.
"""

import numpy as np

def get_initial_white_pixel(grid):
    # Find the coordinates of the initial white pixel (value 0)
    white_pixels = np.argwhere(grid == 0)
    if len(white_pixels) > 0:
        return white_pixels[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the initial white pixel
    initial_white_pixel = get_initial_white_pixel(input_grid)

    if initial_white_pixel is not None:
        white_row, white_col = initial_white_pixel

        # Iterate through the grid
        for r in range(rows):
            for c in range(cols):
                # Change red pixels to white based on the initial white pixel's row and column
                if output_grid[r][c] == 2:  # If it's red
                    if (r == white_row or c == white_col) and not (r == rows // 2 and c == cols // 2):
                      output_grid[r][c] = 0

    return output_grid