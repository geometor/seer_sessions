"""
1. Identify Objects: Find contiguous regions (objects) of non-zero pixels in the input grid.
2. Observe Color Change: For each object, compare its color in the input grid to the color of the corresponding region (same position) in the output grid.
3. Apply Transformation: If the color in the output grid differs from the input, change all pixels within that object in the input grid to the new color.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects (same color and connected) in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, object_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                if object_pixels:
                    objects.append((grid[r, c], object_pixels))
    return objects

def transform(input_grid, output_grid):  # Include output_grid
    # Initialize output_grid
    transformed_grid = np.copy(input_grid)

    # Find objects in the input grid
    input_objects = find_objects(input_grid)

    # Observe color changes and apply the transformation
    for color, pixels in input_objects:
        # Check if the color of *any* pixel in this object has changed
        color_changed = False
        new_color = None
        for r, c in pixels:
            if input_grid[r,c] != output_grid[r,c]:
                color_changed = True
                new_color = output_grid[r,c]
                break

        if color_changed:
            for r,c in pixels:
              transformed_grid[r,c] = new_color

    return transformed_grid