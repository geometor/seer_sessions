"""
1.  **Identify** the gray (5) pixels in the input grid. These remain unchanged in the output.
2.  **Identify** the connected green (3) pixels in the input.
3.  **Hollow** out the original green pixels - expand green pixels in all directions by one cell.
4.  **Fill**: Any cell, not part of any other object (gray or hollowed green object), becomes, or remains, white.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def expand_pixels(grid, pixels):
    """Expands the given pixels by one cell in all directions."""
    expanded_pixels = set()
    for r, c in pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    expanded_pixels.add((nr, nc))
    return list(expanded_pixels)

def transform(input_grid):
    # Initialize output grid with the same dimensions and filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find gray pixels and copy them to the output grid
    gray_pixels = find_pixels(input_grid, 5)
    for r, c in gray_pixels:
        output_grid[r, c] = 5

    # Find green pixels
    green_pixels = find_pixels(input_grid, 3)

    # Expand and hollow the green pixels
    expanded_green_pixels = expand_pixels(input_grid, green_pixels)

    # Draw expanded, hollowed green shape
    for r,c in expanded_green_pixels:
        output_grid[r,c] = 3

    return output_grid