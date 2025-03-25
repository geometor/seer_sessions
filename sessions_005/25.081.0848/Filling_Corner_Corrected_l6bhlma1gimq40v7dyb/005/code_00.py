"""
The transformation rule involves identifying yellow objects and adding red pixels to fill to the edge of the grid on the opposite side, creating a "filled corner" effect.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a specified color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        """Depth-First Search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)

    return objects

def fill_opposite_side(grid, yellow_object):
    """
    Fills red pixels to the opposite edge based on yellow object position.
    """
    output_coords = []
    min_row = min(y for y, x in yellow_object)
    max_row = max(y for y, x in yellow_object)
    min_col = min(x for y, x in yellow_object)
    max_col = max(x for y, x in yellow_object)
    
    # fill to top
    if min_row > 0:
        for c in range(grid.shape[1]):
            for r in range(min_row):
                output_coords.append((r,c))

    # fill to bottom
    if max_row < grid.shape[0]-1:
        for c in range(grid.shape[1]):
          for r in range(max_row+1,grid.shape[0]):
                output_coords.append((r,c))

    # fill to left
    if min_col > 0:
        for r in range(grid.shape[0]):
            for c in range(min_col):
                output_coords.append((r,c))

    # fill to right
    if max_col < grid.shape[1] - 1:
        for r in range(grid.shape[0]):
            for c in range(max_col+1, grid.shape[1]):
                output_coords.append((r,c))


    return output_coords

def transform(input_grid):
    """
    Identifies yellow objects and adds red pixels by filling towards the opposite edges.
    """
    output_grid = np.copy(input_grid)

    # Find yellow objects
    yellow_objects = find_objects(input_grid, 4)
    
    red_coords = []

    # determine extent of the red fill based on boundaries
    for yellow_object in yellow_objects:
        red_coords.extend( fill_opposite_side(input_grid, yellow_object) )

    # fill the red pixels, only if within the yellow object boundary
    for r, c in red_coords:
            output_grid[r, c] = 2

    return output_grid