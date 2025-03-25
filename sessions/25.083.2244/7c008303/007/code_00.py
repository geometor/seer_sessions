"""
Transforms an input grid into an output grid by splitting it along a horizontal azure line, extracting colored objects from above and below the line, combining them by reflecting the x axis, and arranging them into a new grid.
"""

import numpy as np

def get_azure_line_row(grid):
    """Finds the row index of the horizontal azure line."""
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1

def get_objects(grid_section):
    """
    Identifies colored objects in a grid section.
    Returns a dictionary of objects, where keys are colors and values are lists of (row, col) coordinates.
    """
    objects = {}
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid_section.shape[0] and 0 <= c < grid_section.shape[1]

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid_section[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(grid_section.shape[0]):
        for c in range(grid_section.shape[1]):
            color = grid_section[r, c]
            if color != 0 and color != 8 and (r, c) not in visited:
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def reflect_x(coords, width):
    """Reflects coordinates across the x-axis."""
    reflected_coords = []
    for r, c in coords:
        reflected_coords.append((r, width - 1 - c))

    return reflected_coords

def get_bounding_box(coords):
  """
    get smallest bounding box that contains all coordinates
  """
  if not coords:
      return None, None, None, None # No coordinates
  
  min_row = min(r for r, _ in coords)
  max_row = max(r for r, _ in coords)
  min_col = min(c for _, c in coords)
  max_col = max(c for _, c in coords)

  return min_row, max_row, min_col, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)
    azure_line_row = get_azure_line_row(input_grid)

    # Split the grid into top and bottom sections
    top_section = input_grid[:azure_line_row]
    bottom_section = input_grid[azure_line_row + 1:]

    # Get objects from each section
    top_objects = get_objects(top_section)
    bottom_objects = get_objects(bottom_section)
    
    # Calculate maximum width of top and bottom colored objects
    top_width = 0
    for color, object_list in top_objects.items():
      for obj_coords in object_list:
        _,_,min_col,max_col = get_bounding_box(obj_coords)
        width = max_col - min_col + 1
        top_width = max(top_width,width)
        

    bottom_width = 0
    for color, object_list in bottom_objects.items():
      for obj_coords in object_list:
        _,_,min_col,max_col = get_bounding_box(obj_coords)
        width = max_col - min_col + 1
        bottom_width = max(bottom_width,width)

    max_width = max(top_width, bottom_width)

    # Create a combined dictionary of objects, reflecting bottom objects
    combined_objects = {}
    for color, object_list in top_objects.items():
        if color not in combined_objects:
          combined_objects[color] = []
        combined_objects[color].extend(object_list) # add all from the list

    for color, object_list in bottom_objects.items():
        if color not in combined_objects:
            combined_objects[color] = []
        
        reflected_objects = []
        for obj_coords in object_list:
          reflected_objects.append(reflect_x(obj_coords,input_grid.shape[1])) # reflect on original width
        
        combined_objects[color].extend(reflected_objects)

    # Determine output grid dimensions based on bounding boxes of combined objects
    output_rows = []
    output_cols = []

    for color, object_list in combined_objects.items():
        for obj_coords in object_list:
            for r, c in obj_coords:
                output_rows.append(r)
                output_cols.append(c)

    if not output_rows or not output_cols:
        return []  # Empty output if no colored objects

    # Create output grid
    min_output_row = min(output_rows)
    max_output_row = max(output_rows)
    
    min_output_col, max_output_col, _, _ = get_bounding_box(output_cols)
    
    output_width  = max_output_col + 1 #max_width
    output_height = max_output_row - min_output_row + 1

    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Populate output grid
    for color, object_list in combined_objects.items():
        for obj_coords in object_list:
            for r, c in obj_coords:
              if 0 <= c < output_width: # to make sure the reflected object is inside bounds
                output_grid[r - min_output_row, c] = color


    return output_grid.tolist()