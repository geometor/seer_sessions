"""
1.  **Identify Red Pixels:** Find all pixels with the color red (value 2).
2.  **Target Below Pixel:** For each red pixel, locate the pixel directly below it.
3.  **Conditional Change:** If the pixel directly below is white (value 0), change its color to blue (value 1).
4. If the pixel directly below the red pixel has any other color, make no changes.
5. All other pixels retain their color.
"""

import numpy as np

def get_pixel_below(grid, row, col):
    """Gets the coordinates of the pixel directly below the given pixel."""
    rows, _ = grid.shape
    if row + 1 < rows:
        return (row + 1, col)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels.
    for row in range(rows):
        for col in range(cols):
            # Identify red pixels.
            if input_grid[row, col] == 2:
                # Get the pixel directly below.
                below_coords = get_pixel_below(input_grid, row, col)

                # Change color of the below pixel to blue if it is white
                if below_coords:
                    below_row, below_col = below_coords
                    if input_grid[below_row, below_col] == 0:
                        output_grid[below_row, below_col] = 1

    return output_grid