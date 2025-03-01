"""
1.  **Identify** all connected components of green (3) pixels.
2.  **For each** green connected component, **identify** the "internal" green pixels. An internal pixel is defined as a green pixel that is completely surrounded by other green pixels (up, down, left, and right - 4-connectivity). It will not be on the edge of the green region, by definition.
3.  **Change** the color of some of the identified internal green pixels to yellow (4). Starting from the top left, fill horizontally and stop when a different color is hit and do the same vertically and fill vertically.
4.  **Leave** all other pixels unchanged.
"""

import numpy as np

def get_connected_components(grid, color):
    """Finds connected components of a given color."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(r, c, current_component):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_component.append((r, c))
        dfs(r + 1, c, current_component)
        dfs(r - 1, c, current_component)
        dfs(r, c + 1, current_component)
        dfs(r, c - 1, current_component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_component = []
                dfs(r, c, current_component)
                components.append(current_component)
    return components

def is_internal(grid, r, c, color):
    """Checks if a pixel is internal to a connected component."""
    if (r <= 0 or r >= grid.shape[0] - 1 or
        c <= 0 or c >= grid.shape[1] - 1):
        return False  # Check bounds to prevent errors
    
    return (grid[r - 1, c] == color and
            grid[r + 1, c] == color and
            grid[r, c - 1] == color and
            grid[r, c + 1] == color)

def transform(input_grid):
    """Fills the internal regions of green areas with yellow."""
    output_grid = np.copy(input_grid)
    green_components = get_connected_components(input_grid, 3)

    for component in green_components:
        internal_pixels = []
        for r, c in component:
            if is_internal(input_grid, r, c, 3):
                internal_pixels.append((r, c))
        
        #fill horizontally and vertically from top left internal pixel
        if (len(internal_pixels) > 0):
          min_r = min(internal_pixels, key=lambda item: item[0])[0]
          min_c = min(internal_pixels, key=lambda item: item[1])[1]

          for r, c in internal_pixels:
            if r == min_r:
              output_grid[r,c] = 4

          for r, c in internal_pixels:
            if c == min_c:
              output_grid[r,c] = 4
        
    return output_grid