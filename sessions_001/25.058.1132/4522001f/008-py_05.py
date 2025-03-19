"""
1.  **Find the Red Pixel:** Locate the single red pixel (value 2) within the input grid. Record its row and column indices. If no red pixel is present the side length is zero, return the original grid.
2.  **Determine Square Size:** Calculate the side length of the green square. The side length is the maximum of the row and column indices of the red pixel.
3.  **Create Green Square:** In the output grid (which has the same dimensions as the input grid), create a square of green pixels (value 3) in the top-left corner. The side length of this square is determined in step 2.
4.  **Fill Remaining Pixels:** All remaining pixels in the output grid that are not part of the green square are set to white (value 0).
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the locations of all pixels of a given color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input and filled with white (0)
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Find the red pixel
    red_pixels = find_pixels(input_grid, 2)

    # If a red pixel is found, create the green square
    if len(red_pixels) > 0:
        # Get the row and column number of the red pixel
        red_row, red_col = red_pixels[0]

        # Determine the square's side length (maximum of row and column)
        side_length = max(red_row, red_col)

        # Create the green square
        for r in range(side_length):
            for c in range(side_length):
                output_grid[r, c] = 3
    else:
        return input_grid

    return output_grid