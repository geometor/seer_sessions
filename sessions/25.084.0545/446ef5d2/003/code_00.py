"""
1.  **Identify Background:** Determine the background color (color '8' in both examples).
2.  **Identify Objects:** Find all contiguous regions (objects) of pixels with the same color *other than the background color*. Pixels are considered connected if they are adjacent horizontally, vertically, or diagonally.
3.  **Identify Boundaries:** Regions of background color define boundaries.
4. **Shift Objects to Boundary**. Within each bounded area, shift all objects within the area down, until the bottom row within that region is filled, or there is a collision with another non-background object. Do not move any pixels of the boundry color.
"""

import numpy as np

def find_objects(grid, background_color):
    """Finds contiguous regions (objects) of the same color, excluding the background."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects.append({'color': grid[row, col], 'pixels': object_pixels})
    return objects

def find_boundaries(grid, background_color):
    """Finds boundary pixels (pixels of background color)."""
    boundaries = []
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r,c] == background_color:
          boundaries.append((r,c))
    return boundaries

def shift_object_to_boundary(grid, object_pixels, background_color):
    """Shifts an object down within its boundary until blocked."""
    # Create a copy to avoid modifying the original grid during calculations
    grid_copy = np.copy(grid)
    color = grid_copy[object_pixels[0]]

    # Sort by row in descending order for correct shifting
    object_pixels.sort(key=lambda p: p[0], reverse=True)

    # 1. Clear the original object's pixels
    for r, c in object_pixels:
      grid_copy[r,c] = background_color

    # 2. Determine new positions, checking for boundaries and other objects
    new_positions = {}
    rows_shifted = {}

    for r, c in object_pixels:
        if c not in rows_shifted:
          rows_shifted[c] = 0

        new_r = r
        while new_r + 1 < grid.shape[0] and grid_copy[new_r + 1, c] == background_color:
            new_r += 1

        new_positions[(r,c)] = (new_r,c)

        
    # 3. place the objects in the new grid
    for (old_r,old_c),(new_r,new_c) in new_positions.items():
      grid_copy[new_r,new_c] = color


    return grid_copy


def transform(input_grid):
    # 1. Identify Background
    background_color = 8
    output_grid = np.copy(input_grid)

    # 2. Identify Objects
    objects = find_objects(output_grid, background_color)

    # 3. Find boundaries (not explicitly used in the shifting logic itself,
    #    but conceptually important for understanding the problem)
    boundaries = find_boundaries(output_grid, background_color)


    # 4. Shift Objects to Boundary
    for obj in objects:
        output_grid = shift_object_to_boundary(output_grid, obj['pixels'], background_color)

    return output_grid