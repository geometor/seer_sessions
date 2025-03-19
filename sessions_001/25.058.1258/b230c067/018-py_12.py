"""
1.  **Identify the Azure Object:** Locate all contiguous regions of azure (8) pixels in the input grid.
2.  **Recolor the Azure Object:** Change *all* pixels within the identified azure region(s) to blue (1).
3.  **Identify Adjacent Background:** Iterate over the *original* input. For each white (0) pixel *adjacent* to an azure(8) pixel, recolor that pixel to Red (2) in the output.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all contiguous regions of the specified color."""
    visited = set()
    objects = []

    def dfs(r, c):
        """Depth-first search to find contiguous pixels."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return []
        visited.add((r, c))
        region = [(r, c)]
        region.extend(dfs(r + 1, c))
        region.extend(dfs(r - 1, c))
        region.extend(dfs(r, c + 1))
        region.extend(dfs(r, c - 1))
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                objects.append(dfs(r, c))
    return objects

def get_adjacent_background(grid, object_coords):
    """Finds white (0) pixels adjacent to the given object coordinates."""
    adjacent_background = []
    rows, cols = grid.shape
    for r, c in object_coords:
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                adjacent_background.append((nr, nc))
    return adjacent_background


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify the Azure Object(s)
    azure_objects = find_objects(input_grid, 8)

    # 2. Recolor the Azure Object(s)
    for obj in azure_objects:
        for r, c in obj:
            output_grid[r, c] = 1

    # 3. Identify Adjacent Background (using original input) and Recolor
    for obj in azure_objects:  # Iterate through original azure object locations
       adjacent_pixels = get_adjacent_background(input_grid, obj)
       for r, c in adjacent_pixels:
           output_grid[r,c] = 2

    return output_grid