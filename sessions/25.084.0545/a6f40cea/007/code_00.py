"""
Transforms the input grid by identifying specific objects and representing them in the output grid.
The output grid represents a simplified version of selected objects based on height and spatial relationships,
primarily focusing on objects with a height of 1 and specific interactions between objects of mixed heights.
"""

import numpy as np

def find_objects(grid, background_color):
    """
    Finds contiguous regions of the same color (objects) in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    def dfs(r, c, color, object_coords):
        if (r, c) in visited or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for nr, nc in get_neighbors(r, c):
            dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color and (r, c) not in visited:
                object_coords = []
                dfs(r, c, color, object_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_coords)
    return objects

def get_bounding_box(coords):
    """
    Returns the bounding box of a set of coordinates.
    """
    if not coords:
        return (0, 0), (0, 0)
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c), (max_r, max_c)

def split_objects_by_intervening(objects, color):
    """
    Splits objects of a given color into groups based on whether there are intervening objects.
    """
    groups = []
    current_group = []

    sorted_objects = sorted(objects[color], key=lambda obj: get_bounding_box(obj)[0][1])  # Sort by min_col

    for i, obj_coords in enumerate(sorted_objects):
        if not current_group:
            current_group.append(obj_coords)
        else:
            last_obj = current_group[-1]
            (_, last_max_c) = get_bounding_box(last_obj)
            (curr_min_r, curr_min_c), _ = get_bounding_box(obj_coords)

            intervening = False
            for other_color in objects:
                if other_color != color:
                    for other_obj in objects[other_color]:
                        (_, other_min_c), (_, other_max_c) = get_bounding_box(other_obj)
                        if last_max_c < other_min_c < curr_min_c :
                            intervening = True
                            break
                    if intervening:
                        break
            
            if intervening:
                groups.append(current_group)
                current_group = [obj_coords]
            else:
                current_group.append(obj_coords)
    if current_group:
      groups.append(current_group)

    return groups

def transform(input_grid):
    """
    Transforms the input grid based on identified objects and their properties. The output
    represents selected objects, focusing on height-1 objects and interactions.
    """
    grid = np.array(input_grid)
    background_color = grid[0, 0]  # Assume top-left pixel is background

    objects = find_objects(grid, background_color)
    
    selected_objects = {}

    # Select height-1 objects, if all objects of that color are height-1
    for color in list(objects.keys()):
        all_height_one = True
        for obj_coords in objects[color]:
            (min_r, _), (max_r, _) = get_bounding_box(obj_coords)
            if max_r - min_r != 0:
                all_height_one = False
                break
        if all_height_one:
          selected_objects[color] = objects.pop(color)

    # Handle mixed height
    for color in list(objects.keys()):
          object_groups = split_objects_by_intervening(objects, color)          
          selected_objects[color] = []
          for group in object_groups:
            if group:
              selected_objects[color].append(group[0]) # top
            if len(group) > 1:
              selected_objects[color].append(group[-1]) # bottom


    # determine output grid
    output_width = 0
    output_height = 0

    for color in selected_objects:
        for obj_coords in selected_objects[color]:
           (_,min_c), (_, max_c) = get_bounding_box(obj_coords)
           width = max_c - min_c + 1

           (min_r, _), (max_r, _) = get_bounding_box(obj_coords)
           height = max_r - min_r + 1

           if height == 1:
              output_width += 2  # two spaces per
              output_height = max(output_height, len(selected_objects[color]) ) # take the biggest
           else:
              output_width += width
              output_height = max(output_height, height)
    
    output_grid = np.full((output_height, output_width), background_color, dtype=int)
   
    # output objects
    col_offset = 0

    for color in sorted(selected_objects.keys()):
      for obj_coords in selected_objects[color]:
          (min_r, min_c), (max_r, max_c) = get_bounding_box(obj_coords)
          height = max_r - min_r + 1
          width = max_c - min_c + 1

          if height == 1:
            # create 2x1 area, place at row, col offset
            if 0 < output_grid.shape[0] and col_offset < output_grid.shape[1]:
              output_grid[0 : min(2, output_grid.shape[0]), col_offset:col_offset+2] = color
            col_offset += 2
          else:
             # output top row
            for c in range(width):
              if 0 < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
                output_grid[0, c + col_offset] = grid[min_r, min_c + c]

            # output the bottom, conditionally, based on height
            if height > 1:
                bottom_row_index = min(height -1, output_grid.shape[0]-1) # ensure within output bounds
                for c in range(width):                
                    if bottom_row_index < output_grid.shape[0] and c + col_offset < output_grid.shape[1]:
                      output_grid[bottom_row_index, c + col_offset] = grid[max_r, min_c + c]

            col_offset += width
    return output_grid.tolist()