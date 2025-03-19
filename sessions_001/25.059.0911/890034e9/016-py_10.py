"""
1. Identify distinct objects within the input grid. An object is a contiguous block of pixels of the same color.
2. Note the color and position of each object.
3. In the output grid, shift all objects to their diagonally opposite position. Maintain their relative position, and shape.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects.append({
                        'color': grid[row, col],
                        'pixels': object_pixels
                    })
    return objects

def transform(input_grid):
    """Transforms the input grid by shifting objects diagonally."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)  # Initialize with zeros

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Shift objects to their diagonally opposite positions
    for obj in objects:
        for row, col in obj['pixels']:
            new_row = rows - 1 - row
            new_col = cols - 1 - col
            output_grid[new_row, new_col] = obj['color']

    return output_grid