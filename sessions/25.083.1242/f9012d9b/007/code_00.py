"""
1.  **Identify Objects:** Determine all contiguous regions (objects) of the same color in the input grid.
2.  **Case: Single Dominant Color:** If the input grid consists of mostly one color (with at most one other color of only 1 pixel), the output is a 1x1 grid containing the top-left pixel of the input grid.
3.  **Case: Colors 1 and 2:** If the input grid contains both colors 1 and 2:
    *   Locate the largest contiguous region of color 1.
    *   Extract a 2x2 subgrid from the top-left corner of this region.
    *   If the extracted subgrid contains color 2, this is the output.
    *    If color 2 is not present, search for a 2x2 area where colors 1 and 2 exists, return if found.

4.  **Case: Colors 2 and 5 (and no color 1):** If the input grid contains both colors 2 and 5 (and no color 1):
    *    Find the objects with color 2 and 5
    *    Extract the 2x2 subgrid that includes 2 and 5 if exists.
5.  **Default:** In all other cases, or if no suitable subgrid can be found based on the above rules, the transformation is considered invalid and outputs -1.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (regions of same color) in a grid.
    Returns a dictionary where keys are colors and values are lists of object coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def get_object_bounding_box(obj_coords):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) for an object.
    """
    if not obj_coords:
        return None
    min_row = min(coord[0] for coord in obj_coords)
    min_col = min(coord[1] for coord in obj_coords)
    max_row = max(coord[0] for coord in obj_coords)
    max_col = max(coord[1] for coord in obj_coords)
    return min_row, min_col, max_row, max_col

def get_largest_object_by_color(objects, color):
    """
    Finds and returns the largest object of a specific color.
    """
    largest_obj_size = 0
    largest_obj_coords = []

    if color in objects:
        for obj_coords in objects[color]:
            size = len(obj_coords)
            if size > largest_obj_size:
                largest_obj_size = size
                largest_obj_coords = obj_coords

    return largest_obj_coords

def extract_2x2_subgrid(grid, r, c):
  """Extracts a 2x2 subgrid from the input grid, returns None if out of bounds"""
  rows, cols = len(grid), len(grid[0])
  if r + 1 >= rows or c + 1 >= cols:
      return None  # Out of bounds

  subgrid = [
      [grid[r][c], grid[r][c + 1]],
      [grid[r + 1][c], grid[r + 1][c + 1]]
  ]
  return subgrid

def transform(input_grid):
    input_grid_np = np.array(input_grid)
    objects = find_objects(input_grid_np)

    # Case: Single Dominant Color
    color_counts = {}
    for color in objects:
      for obj in objects[color]:
        if color not in color_counts:
          color_counts[color] = 0
        color_counts[color] += len(obj)

    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)

    if len(sorted_colors) == 1 or (len(sorted_colors) == 2 and sorted_colors[1][1] == 1 ):
        return [[input_grid_np[0][0]]]

    # Case: Colors 1 and 2
    if 1 in objects and 2 in objects:
        largest_1_coords = get_largest_object_by_color(objects, 1)
        bbox_1 = get_object_bounding_box(largest_1_coords)
        subgrid = extract_2x2_subgrid(input_grid_np, bbox_1[0], bbox_1[1])

        if subgrid:
          subgrid_np = np.array(subgrid)
          if 2 in subgrid_np:
            return subgrid

        # Search for any 2x2 containing 1 and 2:
        for r in range(input_grid_np.shape[0]):
          for c in range(input_grid_np.shape[1]):
            subgrid = extract_2x2_subgrid(input_grid_np, r,c)
            if subgrid:
              subgrid_np = np.array(subgrid)
              if 1 in subgrid_np and 2 in subgrid_np:
                return subgrid

    # Case: Colors 2 and 5 (and no color 1)
    if 2 in objects and 5 in objects and 1 not in objects:

        # Search for any 2x2 containing 2 and 5
        for r in range(input_grid_np.shape[0]):
            for c in range(input_grid_np.shape[1]):
                subgrid = extract_2x2_subgrid(input_grid_np, r, c)
                if subgrid:
                  subgrid_np = np.array(subgrid)
                  if 2 in subgrid_np and 5 in subgrid_np:
                    return subgrid


    # Default
    return [[-1]]