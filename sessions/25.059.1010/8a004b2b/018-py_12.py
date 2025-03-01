"""
Transforms an input grid by extracting a column section defined by the positions of yellow objects, preserving the colors and their relative vertical positions within that column. If only azure objects are present, it creates a single row containing all azure segments.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored rectangular blocks in the grid."""
    objects = {}
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                if color not in objects:
                    objects[color] = []
                obj_coords = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and (curr_r, curr_c) not in visited:
                        visited.add((curr_r, curr_c))
                        obj_coords.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects[color].append(obj_coords)
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box of a list of coordinates."""
    min_r = min(c[0] for c in coords)
    max_r = max(c[0] for c in coords)
    min_c = min(c[1] for c in coords)
    max_c = max(c[1] for c in coords)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine output based on object presence
    if 4 in objects:  # Yellow exists, extract column section
      yellow_coords = []
      for obj in objects[4]:
        yellow_coords.extend(obj)
      (min_r, min_c), (max_r, max_c) = get_bounding_box(yellow_coords)
      output_height = max_r - min_r + 1
      output_grid = np.zeros((output_height, 1), dtype=int)
      
      # copy column from input to output, based on yellow position
      for r in range(min_r, max_r + 1):
          color = input_grid[r, min_c]
          if color != 0:
            output_grid[r - min_r, 0] = color

    elif 8 in objects and len(objects) == 1:  # Only azure, create a combined row
        all_coords = []
        for obj in objects[8]:
            all_coords.extend(obj)
        (min_r, min_c), (max_r, max_c) = get_bounding_box(all_coords)
        output_width = max_c - min_c + 1
        output_grid = np.zeros((1, output_width), dtype=int)
        for c in range(output_width):
          output_grid[0,c] = 8 # input always has only 8

    else: # no yellow or just azure
        return np.zeros((1,1), dtype=int)


    return output_grid