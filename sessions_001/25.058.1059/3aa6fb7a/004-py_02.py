"""
Identifies azure colored shapes and changes the color of the rightmost pixel of the bottom row of the azure shape to blue.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color and not visited[i, j]:
                object_pixels = []
                stack = [(i, j)]
                visited[i, j] = True

                while stack:
                    x, y = stack.pop()
                    object_pixels.append((x, y))

                    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    for nx, ny in neighbors:
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] == color and not visited[nx, ny]:
                            stack.append((nx, ny))
                            visited[nx, ny] = True
                objects.append(object_pixels)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = input_grid.copy()
    azure_objects = find_objects(input_grid, 8)

    for obj in azure_objects:
        # Find the bottom row of the object.
        bottom_row = max(x for x, y in obj)
        
        # Find the rightmost pixel in the bottom row.
        bottom_row_pixels = [(x, y) for x, y in obj if x == bottom_row]
        rightmost_pixel = max(bottom_row_pixels, key=lambda p: p[1])

        # Change the color of the rightmost pixel to blue.
        output_grid[rightmost_pixel] = 1

    return output_grid