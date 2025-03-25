```python
"""
Removes single-colored edge objects and creates a rectangle at the bottom of the grid using a color from a multi-colored edge object.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def is_edge_object(obj, rows, cols):
    """Checks if an object touches any edge of the grid."""
    for r, c in obj:
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return True
    return False

def is_single_colored_object(grid, obj):
    """Checks if an object contains only one color."""
    if not obj:
        return False

    first_pixel_color = grid[obj[0][0], obj[0][1]]
    for r, c in obj:
        if grid[r, c] != first_pixel_color:
            return False
    return True


def get_bottom_center_multicolored_object(grid, objects):
    """
    Finds the multi-colored object closest to the bottom and center.
    """
    rows, cols = grid.shape
    bottom_center_objects = []
    for obj in objects:
        # should be multicolored and edge object
        if not is_single_colored_object(grid, obj) and is_edge_object(obj, rows, cols):
            min_row = rows
            for r,c in obj:
                if r < min_row:
                    min_row = r

            if min_row > rows//2:
              bottom_center_objects.append(obj)

    if not bottom_center_objects:
        return None
    
    if len(bottom_center_objects) > 1:
      #get the one more to the bottom
      max_r = -1
      selected_object = None
      for obj in bottom_center_objects:
        for r,c in obj:
          if r > max_r:
            max_r = r
            selected_object = obj
      return selected_object

    return bottom_center_objects[0]

def get_replacement_color(grid, obj):
    """
    Gets the most frequent color from the object.
    """

    color_counts = {}
    for r,c in obj:
        color = grid[r, c]
        if color != 0:
          if color not in color_counts:
              color_counts[color] = 0
          color_counts[color] += 1
    
    most_frequent_color = 0
    max_count = 0

    for color, count in color_counts.items():
      if count > max_count:
        max_count = count
        most_frequent_color = color

    return most_frequent_color

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find objects
    objects = find_objects(grid)

    # Remove single-colored edge objects
    for obj in objects:
        if is_single_colored_object(grid, obj) and is_edge_object(obj, rows, cols):
            for r, c in obj:
                grid[r,c] = 0

    # re-calculate objects
    objects = find_objects(grid)
    # Get bottom center multi colored object
    target_object = get_bottom_center_multicolored_object(grid, objects)

    # proceed if valid target object
    if target_object:

        # get replacement color from target object
        replacement_color = get_replacement_color(grid, target_object)

        # get lowest row from target_object
        max_row = 0
        for r,c in target_object:
          if r > max_row:
            max_row = r

        # Create rectangle
        rectangle_height = 3
        
        y_start = max_row - rectangle_height + 1 # inclusive
        if y_start < 0:
            y_start = 0

        x_coords = [c for r, c in target_object]
        min_x = min(x_coords)
        max_x = max(x_coords)
        
        for r in range(y_start, y_start + rectangle_height):
            for c in range(min_x, max_x + 1):
              output_grid[r,c] = replacement_color

    return output_grid.tolist()
```