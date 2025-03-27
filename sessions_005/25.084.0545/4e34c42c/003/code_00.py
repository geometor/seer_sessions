"""
Identifies objects in the input grid, identifies a target object, and constructs a new grid by combining and arranging rows based on the colors and positions of pixels within the objects.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_background_colors(grid, objects):
    """
    Get background color by finding largest objects
    """
    objects_by_size = sorted(objects, key=len, reverse=True)
    background_colors = []
    for obj in objects_by_size:
      if len(obj) > .10 * grid.size:
        background_colors.append(grid[obj[0][0], obj[0][1]])
    return background_colors


def find_target_object(grid, objects):
    """
    Finds set of objects, excluding background
    """
    # Find background color
    background_colors = get_background_colors(grid, objects)

    # Find the colors
    colors = set()
    for obj in objects:
      for r,c in obj:
        color = grid[r,c]
        if color not in background_colors:
          colors.add(color)

    # Find target objects in the top half
    top_half_objects = []
    for obj in objects:
        min_row = min(r for r, _ in obj)
        if min_row < grid.shape[0] / 2:
          top_half_objects.append(obj)

    # Filter for objects containing all colors
    target_object_candidates = []
    for obj in top_half_objects:
        obj_colors = set()
        for r,c in obj:
          obj_colors.add(grid[r,c])
        if obj_colors.issuperset(colors):
          target_object_candidates.append(obj)
    # combine objects
    target_object = []
    if target_object_candidates:
      for obj in target_object_candidates:
        target_object.extend(obj)

    return target_object if target_object else None

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Find background
    background_colors = get_background_colors(input_grid, objects)

    # Identify target object
    target_object = find_target_object(input_grid, objects)

    if target_object is None:
      return [[]]

    # Get colors of target object
    target_colors = set()
    for r, c in target_object:
        target_colors.add(input_grid[r, c])

    # 1. First Row
    first_row_pixels = []
    # Get the min row of the target object
    min_target_row = min(r for r, _ in target_object)

    for obj in objects:
      for r, c in obj:
        # Check it's the right color and in the first row of the target object
        if input_grid[r,c] in target_colors and any(r==min_target_row and c == col for row, col in target_object):
          first_row_pixels.append((r,c))

    # Sort first row by column
    first_row_pixels.sort(key=lambda x: x[1])
    first_row = [input_grid[r, c] for r, c in first_row_pixels]

    # 2. Middle Rows (3 identical)
    middle_rows = []
    middle_row_pixels = []
    for color in sorted(target_colors):
        if color not in first_row:
            for r, c in target_object:
                if input_grid[r, c] == color:
                    middle_row_pixels.append((r,c))

    middle_row_pixels.sort(key=lambda x: x[1])
    middle_row = [input_grid[r, c] for r, c in middle_row_pixels]


    for _ in range(3):
        middle_rows.append(middle_row)


    # 3. Last Row (copy of first)
    last_row = first_row

    # Combine all rows for output
    output_grid_list = [first_row] + middle_rows + [last_row]

    # Find max width
    max_width = max(len(row) for row in output_grid_list) if output_grid_list else 0


    # Create the output grid
    output_grid = np.zeros((len(output_grid_list), max_width), dtype=int)

    for row_idx, row_pixels in enumerate(output_grid_list):
      for col_idx, pixel in enumerate(row_pixels):
          output_grid[row_idx, col_idx] = pixel

    return output_grid.tolist()