"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of the same non-zero color within the input grid.

2.  **Locate the right-most edge:** Locate the right-most side of all objects.

3.  **Conditional Filling:** For all objects, fill color magenta (6) from the spatial relationship until encountering the background (0).

4.  **Preserve Grid:** Maintain the original dimensions of the grid. All pixels not affected by the filling rule retain their original color from the input.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions (objects) of the same non-zero color.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = set()
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def find_rightmost_edge(obj):
    """
    Finds the rightmost coordinates of an object.

    Args:
        obj: set{(r,c)}

    Returns:
        list: the points on the rightmost side of an object
    """

    # sort to put them in the right order
    coords = sorted(list(obj))

    max_col = -1
    for r, c in coords:
      if c > max_col:
        max_col = c

    rightmost = []
    for r,c in coords:
      if c == max_col:
        rightmost.append( (r,c) )

    return rightmost
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    objects = find_objects(grid)

    for obj in objects:
        # find the rightmost side
        rightmost_coordinates = find_rightmost_edge(obj)

        # fill in magenta to the left of the rightmost edge
        for r, c in rightmost_coordinates:

          # traverse left
          for i in range(c-1,-1,-1):
            if output_grid[r,i] == 0:
              break
            output_grid[r, i] = 6

    return output_grid.tolist()