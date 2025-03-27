"""
Transforms the input grid by selectively changing the color of certain objects based on their position and connectivity. The transformation identifies one instance of each color (excluding the background colors 7, 8, and 9) and preserves it, while changing the color of other connected objects of the same color. The color changes follow specific rules: 1 becomes 3, and 0, 4, or 6 become 5. Colors 2, 3, and 7 remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects in the grid.  Includes diagonal connections.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        # Include diagonal neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if (r, c) not in visited and color not in [7, 8, 9]:
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def transform(input_grid):
    """
    Applies the transformation to the input grid.
    """
    grid = np.array(input_grid)  # Convert to numpy array for easier manipulation
    output_grid = np.copy(grid)  # Initialize output_grid as a copy of input_grid
    objects = find_objects(grid)

    for color, obj_list in objects.items():
      if not obj_list:
        continue

      # Select the *first* object in the list as the one to preserve
      preserved_obj = obj_list[0]

      # iterate through other objects to change color
      for obj in obj_list:
        if obj != preserved_obj: # do not recolor the preserved object
          for r,c in obj:
            if color == 1:
              output_grid[r][c] = 3
            elif color in [0,4,6]:
              output_grid[r][c] = 5

    return output_grid.tolist()