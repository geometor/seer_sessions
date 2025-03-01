"""
1.  Identify Objects: Locate all contiguous regions (objects) that contain *both* yellow (4) and red (2) pixels.  "Contiguous" means pixels are connected horizontally or vertically, not diagonally.
2.  Transform within Objects:  *Within each identified object*, change *all* red (2) pixels to yellow (4).
3.  Preserve Background: Do not modify any pixels that are not part of the identified objects.
"""

import numpy as np

def find_objects(grid, colors):
    """
    Finds contiguous regions (objects) of specified colors in the grid.
    Returns a list of pixel coordinates for each object.
    "Contiguous" means pixels are connected horizontally or vertically (not diagonally)
    An object *must* contain at least one of each color.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object, color_set):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] not in colors:
            return
        visited[r, c] = True
        current_object.append((r, c))
        color_set.add(grid[r,c])

        # Explore adjacent pixels (horizontally and vertically)
        dfs(r + 1, c, current_object, color_set)
        dfs(r - 1, c, current_object, color_set)
        dfs(r, c + 1, current_object, color_set)
        dfs(r, c - 1, current_object, color_set)


    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] in colors and not visited[r, c]:
                current_object = []
                color_set = set()
                dfs(r, c, current_object, color_set)
                # only add object to list if it has all colors
                if all(color in color_set for color in colors):
                  objects.append(current_object)
    return objects

def transform(input_grid):
    # Create a copy to serve as the output grid
    output_grid = np.copy(input_grid)

    # Find objects containing both yellow (4) and red (2)
    objects = find_objects(input_grid, [2, 4])

    # Transform all red pixels within each object to yellow
    for obj in objects:
        for r, c in obj:
            if output_grid[r, c] == 2:  # If pixel is red
                output_grid[r, c] = 4  # Change to yellow

    return output_grid