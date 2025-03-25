"""
Extracts the unique colors of objects in a 2D grid, preserving the order of their first appearance from top to bottom.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects within the grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of sets, where each set contains the coordinates of an object's pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.add((r, c))

        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = set()
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid to extract unique object colors in order of appearance.

    Args:
      input_grid:  list of lists
    """
    grid = np.array(input_grid)
    objects = get_objects(grid)

    # Extract unique colors in order of object appearance
    ordered_colors = []
    for obj in objects:
        # Get the color of the first pixel in the object (all pixels in an object have the same color)
        first_pixel_coords = next(iter(obj))
        color = grid[first_pixel_coords]
        if color not in ordered_colors:
            ordered_colors.append(color)

    return ordered_colors