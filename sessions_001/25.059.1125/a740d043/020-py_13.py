"""
Locate the single orange pixel (color 7) within the input grid. Extract a block
from the input grid such that the orange pixel is in the top-left corner of the
block. The dimensions of the block are determined by the position of the orange
pixel relative to the grid boundaries. If a 2x2 block can be formed, it is
extracted. Otherwise, a smaller block (1x2, 2x1, or 1x1) is extracted, taking
what is available in the row and column of the orange pixel.
"""

import numpy as np

def find_orange_pixel(grid):
    """Finds the coordinates of the orange pixel (color 7)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                return (r, c)
    return None

def transform(input_grid):
    """Extracts a block with the orange pixel at the top-left."""

    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the coordinates of the orange pixel
    orange_pixel_coords = find_orange_pixel(input_grid)

    if orange_pixel_coords:
        r, c = orange_pixel_coords
        rows, cols = input_grid.shape

        # Determine the size of the extractable block
        height = min(2, rows - r)
        width = min(2, cols - c)

        output_grid = input_grid[r:r+height, c:c+width]
    else:
        output_grid = np.array([])  # Default: empty grid if no orange pixel

    return output_grid.tolist()