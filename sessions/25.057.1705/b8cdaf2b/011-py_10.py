"""
1. Identify the azure rectangle: In the input grid, locate the azure rectangle.
2. Move the azure rectangle up:  Translate the entire azure rectangle upwards by two rows.
3. Create green corners: Create four green pixels at the four corners of the output, excluding the first row. Specifically: row 1, col 0; row 1, col 9; row 2, col 1; and row 2, col 8.
"""

import numpy as np

def get_objects(grid):
    """Identifies distinct objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] != 0:
                color = grid[i, j]
                object_coords = []
                queue = [(i, j)]
                visited[i, j] = True

                while queue:
                    x, y = queue.pop(0)
                    object_coords.append((x, y))

                    # Check adjacent cells (up, down, left, right)
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and \
                           not visited[nx, ny] and grid[nx, ny] == color:
                            queue.append((nx, ny))
                            visited[nx, ny] = True

                objects.append({
                    "color": color,
                    "coordinates": object_coords,
                    "min_row": min(y for x,y in object_coords),
                    "max_row": max(y for x,y in object_coords),
                    "min_col": min(x for x,y in object_coords),
                    "max_col": max(x for x,y in object_coords),
                })

    return objects

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    input_objects = get_objects(input_grid)
    
    # Find the azure rectangle
    azure_rectangle = None
    for obj in input_objects:
      if obj['color'] == 8:
        azure_rectangle = obj
        break

    # Move azure rectangle up by 2
    if azure_rectangle:
        for x, y in azure_rectangle['coordinates']:
            new_row = x - 2
            if new_row >= 0:  # Ensure we don't go out of bounds
               output_grid[new_row, y] = 8

    # Create green corners
    output_grid[1, 0] = 3
    output_grid[1, 9] = 3
    output_grid[2, 1] = 3
    output_grid[2, 8] = 3

    return output_grid