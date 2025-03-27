"""
Transforms the input grid by selectively changing the color of certain objects based on their position and connectivity. The transformation identifies the top-left-most instance of each color (excluding the background colors 7, 8, and 9) and may preserve it or change it to a specific color, while changing the color of other connected objects of the same color. The color changes follow specific rules: The top-left-most 1 becomes 3, and the other objects of color 0, 4, or 6 become 5. Colors 2, 3, and 7 remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects in the grid. Includes diagonal connections.
    Returns a dictionary where keys are colors and values are lists of objects.
    Each object is a list of (row, col) tuples.
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
            if (r, c) not in visited:
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def find_top_left_object(objects_of_a_color):
    """
    Finds the top-left-most object within a list of objects of the same color.
    """
    if not objects_of_a_color:
        return None
    
    min_row = float('inf')
    min_col = float('inf')
    top_left_object = None

    for obj in objects_of_a_color:
        for r, c in obj:
          if r < min_row:
            min_row = r
            min_col = c
            top_left_object = obj
          elif r == min_row: # same row, check col
            if c < min_col:
              min_col = c
              top_left_object = obj

    return top_left_object

def transform(input_grid):
    """
    Applies the transformation to the input grid.
    """
    grid = np.array(input_grid)  # Convert to numpy array
    output_grid = np.copy(grid)
    objects = find_objects(grid)

    # Determine background color (7, 8, or 9, whichever exists)
    background_color = None
    for color in [7, 8, 9]:
        if color in objects:
            background_color = color
            break


    for color, obj_list in objects.items():
      if color == background_color or not obj_list:
          continue
      
      top_left_obj = find_top_left_object(obj_list)

      for obj in obj_list:
        if obj is top_left_obj:
          for r, c in obj:
            if color == 1:
              output_grid[r][c] = 3  # Change top-left 1 to 3
        else:
          # recolor other instances
            for r, c in obj:
                if color in [0, 4, 6]:
                    output_grid[r][c] = 5  # Change 0, 4, 6 to 5

    return output_grid.tolist()