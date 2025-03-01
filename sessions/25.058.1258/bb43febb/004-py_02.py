"""
1.  **Identify Gray Objects:** Locate all contiguous blocks of gray (5) pixels. A contiguous block is defined as a set of pixels of the same color that are connected horizontally or vertically.

2.  **Inner area fill** For all gray areas,
    Locate pixels along the boundary of the object. This forms a rectangle.
    Change the color of the non-boundary pixels, inside the rectangle, to red (2).

3. Preserve all white space (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a specified color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
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

def get_object_bounds(obj):
    """returns to top, left, bottom, right of object"""
    rows = [p[0] for p in obj]
    cols = [p[1] for p in obj]
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    # Create output grid as a copy of input grid.
    output_grid = np.copy(input_grid)
    # Find gray objects
    gray_objects = find_objects(input_grid, 5)

    # Iterate through the gray objects
    for obj in gray_objects:
      # find boundary
      top, left, bottom, right = get_object_bounds(obj)

      # fill inner area
      for row in range(top+1, bottom):
        for col in range(left+1, right):
          output_grid[row,col] = 2
    
    return output_grid