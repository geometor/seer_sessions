"""
1.  **Identify Seed Pixels:** Locate all pixels in the input grid that are not white (color value not equal to 0). These are the "seed" pixels.

2.  **Construct Cross Shapes:** For each seed pixel:
    *   If the position of the seed pixel is on the edge of the grid, extend a line of blue (value 1) of length 1 in the available direction.
    *   If the position of the seed pixel is not on the edge of the grid, create a "cross" or "+" shape centered on the seed pixel using blue pixels (value 1), with lines in all four cardinal directions. Each arm of the cross will have length one, and the shape consists in the pixels that are at distance one. The center point of the cross coincides with the position of the seed.
    *   The original seed pixel value in retained in the output grid.

3. **Other Pixels**: Every other pixel that is not involved in any transformation remain the same, with value 0 (color white).
"""

import numpy as np

def get_seed_pixels(grid):
    # Find coordinates of non-white pixels
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get seed pixels
    seed_pixels = get_seed_pixels(input_grid)

    # change output pixels 
    for r, c in seed_pixels:
        # Keep the original seed pixel
        output_grid[r, c] = input_grid[r,c]

        # Construct cross shapes with blue (1) around seeds, handle edges cases
        if r > 0:
          output_grid[r - 1, c] = 1  # Up
        if r < rows - 1:
          output_grid[r + 1, c] = 1  # Down
        if c > 0:
          output_grid[r, c - 1] = 1  # Left
        if c < cols - 1:
          output_grid[r, c + 1] = 1  # Right

    return output_grid