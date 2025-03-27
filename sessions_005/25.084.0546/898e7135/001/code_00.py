"""
Transforms the input grid by combining colors based on a priority and simplifying shapes to rectangles.
Green (3) dominates all other colors. If no green, other colors combine based on a hierarchy.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous blocks of the same color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj):
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
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def get_bounding_box(obj):
    """Calculates the bounding box for set of pixels

    Args:
        obj (list): list of tuples, with the x and y coordinates

    Returns:
        tuple: coordinates of bounding box (min_row, min_col, max_row, max_col)
    """
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Transforms the input grid based on color priority and simplification to rectangles.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = get_objects(input_grid)

    # Check for dominance of Green (3)
    for color, _ in objects:
        if color == 3:
            output_grid[:] = 3
            return output_grid.tolist()

    # remove colors 0, 7, and 9
    objects = [(c, o) for c, o in objects if c not in [0,7,9]]
    
    if not objects:
      return output_grid.tolist()

    # Color combination hierarchy
    color_priority = [1, 6, 4, 5, 8, 2]
    combined_color = None

    for priority_color in color_priority:
        for color, obj in objects:
          if color == priority_color:
            combined_color = priority_color
            break
        if combined_color is not None:
          break

    if combined_color is None:
        combined_color=objects[0][0]
    
    for color, obj in objects:
      min_row, min_col, max_row, max_col = get_bounding_box(obj)
      output_grid[min_row:max_row+1, min_col:max_col+1] = combined_color
    
    return output_grid.tolist()