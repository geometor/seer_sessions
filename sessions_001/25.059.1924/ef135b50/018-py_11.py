"""
1.  **Identify** all white pixels (value 0) in the input grid.
2.  **Inspect** each identified white pixel.
3.  **Check** if the white pixel is adjacent (horizontally or vertically, but *not* diagonally) to a red pixel (value 2).
4.  **If** a white pixel is adjacent to a red pixel, change its color to maroon (value 9).
5.  **If** a while pixel is not adjacent to any red pixel, leave as original color(0)
6. **Output** new grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the adjacent pixels of a given cell (horizontally and vertically)."""
    rows, cols = grid.shape
    adjacent_pixels = []
    
    if row > 0:
        adjacent_pixels.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))  # Down
    if col > 0:
        adjacent_pixels.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))  # Right
    
    return adjacent_pixels

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Identify white pixels (value 0)
            if input_grid[row, col] == 0:
                # Get adjacent pixels
                adjacent = get_adjacent_pixels(input_grid, row, col)
                # Check for adjacency to a red pixel (value 2)
                for r, c in adjacent:
                    if input_grid[r, c] == 2:
                        # Change color to maroon (value 9)
                        output_grid[row, col] = 9
                        break  # Once changed, no need to check other neighbors

    return output_grid