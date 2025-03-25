```python
"""
The transformation rule involves identifying yellow objects and extending lines of red pixels from the ends of lines formed by yellow pixels. The extension continues in the direction of the line until the edge of the grid is reached. Objects are treated independently.
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

def extend_lines(grid, yellow_object):
    """
    Extends lines from the endpoints of lines within the yellow object.
    """
    red_extensions = []

    # Check for horizontal and vertical lines
    rows = {}
    cols = {}
    for y, x in yellow_object:
        if y not in rows:
            rows[y] = []
        rows[y].append(x)
        if x not in cols:
            cols[x] = []
        cols[x].append(y)
    
    # Extend horizontal lines
    for row, col_list in rows.items():
        col_list.sort()
        if len(col_list) > 0:
          #extend left
          for c in range(col_list[0]-1, -1, -1):
            red_extensions.append((row,c))
          #extend right
          for c in range(col_list[-1]+1, grid.shape[1]):
            red_extensions.append((row,c))
            
    # Extend vertical lines
    for col, row_list in cols.items():
      row_list.sort()
      if len(row_list) > 0:
          # Extend up
          for r in range(row_list[0] - 1, -1, -1):
              red_extensions.append((r, col))
          # Extend down
          for r in range(row_list[-1] + 1, grid.shape[0]):
              red_extensions.append((r, col))
    
    return red_extensions


def transform(input_grid):
    """
    Identifies yellow objects and extends lines of red pixels from endpoints
    of any lines formed by the yellow objects. Extends until a boundary.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # For each yellow object, extend lines from endpoints
    for yellow_object in yellow_objects:
        red_coords = extend_lines(input_grid, yellow_object)
        for r, c in red_coords:
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:  # Boundary check
                output_grid[r, c] = 2

    return output_grid
```