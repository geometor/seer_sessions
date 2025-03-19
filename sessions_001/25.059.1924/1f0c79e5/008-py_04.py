"""
1.  **Initialize Output:** Create an output grid with the same dimensions as the input grid, filled entirely with white pixels (0).

2.  **Find All Non-Zero Pixels:** Iterate through *every* pixel in the input grid. Identify *all* pixels with a value other than 0 (non-white pixels).

3.  **For Each Non-Zero Pixel:** For *each* non-zero pixel found in the input grid:
    a.  **Create Yellow Square:** Create a 3x3 square of yellow pixels (value 4).
    b.  **Center Square:** Determine the location to center the 3x3 yellow square, aligning it with the row and column of the current non-zero pixel.
    c. **Bounds Check:** If centering the square would place any part of it outside the grid boundaries, adjust the position. "Push" the square to the edge of the grid, make sure it remains entirely within the bounds.
    d. **Place Square:** Copy the 3x3 yellow square to output grid at computed (and adjusted) position

4.  **Return:** Return the output grid.
"""

import numpy as np

def _find_non_zero_pixels(grid):
    """Finds coordinates of all non-zero pixels in a grid."""
    rows, cols = grid.shape
    non_zero_pixels = []
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                non_zero_pixels.append((i, j))
    return non_zero_pixels

def _place_yellow_square(grid, center_row, center_col):
    """Places a 3x3 yellow square on the grid, handling boundary conditions."""
    rows, cols = grid.shape
    start_row = max(0, center_row - 1)
    start_col = max(0, center_col - 1)
    end_row = min(rows, center_row + 2)
    end_col = min(cols, center_col + 2)

    start_row = end_row - 3
    start_col = end_col - 3
    

    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            grid[i, j] = 4


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all non-zero pixels
    non_zero_pixels = _find_non_zero_pixels(input_grid)

    # For each non-zero pixel, place a 3x3 yellow square
    for row, col in non_zero_pixels:
        _place_yellow_square(output_grid, row, col)

    return output_grid