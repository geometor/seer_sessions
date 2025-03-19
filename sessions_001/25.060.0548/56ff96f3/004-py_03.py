"""
1.  **Identify Objects:** Find all non-zero pixels (colored pixels) in the input grid. Each contiguous block of the same color is considered an object.
2.  **Horizontal Expansion (Primary):** Each object expands horizontally to the maximum extent possible within the grid. This expansion stops if it encounters a non-zero pixel of a *different* color or the edge of the grid.
3.  **Vertical Expansion (Secondary):** After horizontal expansion, each object expands vertically. The expansion occurs across the *entire height* of the grid. The vertical expansion maintains the horizontal width achieved in step 2. Vertical expansion happens for *all* colored objects.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """Finds the coordinates of all non-zero pixels in a grid."""
    pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                pixels.append((r, c, grid[r, c]))
    return pixels

def expand_horizontally(grid, pixels):
    """Expands pixels horizontally to the maximum extent."""
    expanded_grid = np.zeros_like(grid)
    for r, c, color in pixels:
        # Find leftmost boundary
        left = c
        while left > 0 and grid[r, left - 1] == 0:
            left -= 1

        # Find rightmost boundary
        right = c
        while right < grid.shape[1] - 1 and grid[r, right + 1] == 0:
            right += 1

        # Fill horizontally
        expanded_grid[r, left:right+1] = color
    return expanded_grid

def expand_vertically(grid, expanded_grid):
    """Expands blocks vertically across the entire grid height."""
    final_grid = np.copy(expanded_grid)  # Start with the horizontally expanded grid
    rows, cols = grid.shape

    for c in range(cols):
        for r in range(rows):
            color = expanded_grid[r,c]
            if color != 0:
                final_grid[:,c] = color # fill column
                break # move onto next column

    return final_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find non-zero pixels
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # Expand horizontally
    expanded_grid = expand_horizontally(input_grid, nonzero_pixels)

    # Expand vertically
    output_grid = expand_vertically(input_grid, expanded_grid)

    return output_grid