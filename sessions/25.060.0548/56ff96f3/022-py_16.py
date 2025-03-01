"""
The transformation identifies yellow pixels in the input grid and expands them vertically to form connected regions.
Yellow pixels are considered connected if they are vertically or diagonally adjacent. The vertical expansion covers the
entire vertical range spanned by the connected yellow pixels.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow pixels in the grid."""
    yellow_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def get_connected_components(pixels):
    """Groups yellow pixels into connected components based on vertical/diagonal adjacency."""
    components = []
    visited = set()

    def is_connected(p1, p2):
        """Checks if two pixels are vertically or diagonally adjacent."""
        return abs(p1[0] - p2[0]) <= 1 and abs(p1[1] - p2[1]) <= 1

    def dfs(pixel, current_component):
        """Performs depth-first search to find connected pixels."""
        visited.add(pixel)
        current_component.append(pixel)
        for other_pixel in pixels:
            if other_pixel not in visited and is_connected(pixel, other_pixel):
                dfs(other_pixel, current_component)

    for pixel in pixels:
        if pixel not in visited:
            new_component = []
            dfs(pixel, new_component)
            components.append(new_component)
    return components

def transform(input_grid):
    """
    Transforms the input grid by identifying connected yellow pixels and expanding them vertically.
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find yellow pixels
    yellow_pixels = get_yellow_pixels(input_grid)

    # Group into connected components
    components = get_connected_components(yellow_pixels)

    # Vertical expansion
    for component in components:
        min_row = min(p[0] for p in component)
        max_row = max(p[0] for p in component)
        for pixel in component:
          for r in range(min_row, max_row + 1):
            output_grid[r, pixel[1]] = 4

    return output_grid