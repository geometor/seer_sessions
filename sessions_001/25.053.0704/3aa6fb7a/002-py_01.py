"""
The transformation identifies two azure objects in the grid and in each object, replaces the most top right pixel to blue. The modified objects are then placed in the output grid, maintaining their original positions and other pixel colors.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def find_top_right_pixel(object_pixels):
    # Sort by row (ascending) then by column (descending)
    sorted_pixels = sorted(object_pixels, key=lambda x: (x[0], -x[1]))
    return sorted_pixels[0]


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)

    # Change the color of the top-right pixel of each azure object to blue
    for obj in azure_objects:
      top_right_pixel = find_top_right_pixel(obj)
      output_grid[top_right_pixel]=1

    return output_grid