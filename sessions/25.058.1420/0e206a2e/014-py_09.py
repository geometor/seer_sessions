"""
The transformation rule involves identifying colored objects in the input grid and repositioning them in the output grid based on a set of rules dependent on their row position and color. Objects below row 6 are moved to the bottom, combining objects of colors 1 and 8. Other objects are placed above these, maintaining relative horizontal positions.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a dictionary of objects in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, color, obj_id):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] != color:
            return []

        visited.add((row, col))
        pixels = [(row, col)]

        pixels.extend(dfs(row + 1, col, color, obj_id))
        pixels.extend(dfs(row - 1, col, color, obj_id))
        pixels.extend(dfs(row, col + 1, color, obj_id))
        pixels.extend(dfs(row, col - 1, color, obj_id))

        return pixels

    obj_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                obj_count += 1
                obj_id = f"obj_{obj_count}"
                pixels = dfs(r, c, grid[r][c], obj_id)
                objects[obj_id] = {
                    'color': grid[r][c],
                    'pixels': pixels
                }
    return objects

def object_properties(objects):
    """Computes and adds bounding box and centroid to each object's properties."""
    object_data = {}
    for obj_id, obj in objects.items():
        pixels = obj['pixels']
        if not pixels:
            continue
        min_row = min(p[0] for p in pixels)
        max_row = max(p[0] for p in pixels)
        min_col = min(p[1] for p in pixels)
        max_col = max(p[1] for p in pixels)
        centroid_row = (min_row + max_row) / 2.0
        centroid_col = (min_col + max_col) / 2.0
        object_data[obj_id] = {
            'color': obj['color'],
            'size': len(pixels),
            'bounding_box': (min_row, min_col, max_row, max_col),
            'centroid': (centroid_row, centroid_col),
            'pixels': pixels,
            'min_row': min_row,
            'max_row': max_row,
        }
    return object_data

def combine_pixels(objects, colors):
    """Combines pixels of specified colors from a list of objects."""
    combined_pixels = []
    for obj_id, obj in objects.items():
      if obj['color'] in colors:
        combined_pixels.extend(obj['pixels'])
    return combined_pixels

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Identify Objects and their properties
    objects = get_objects(input_grid)
    object_data = object_properties(objects)
    
    # Determine bottom row for objects moved to the bottom
    bottom_row = rows -1

    # Combine and position objects of color 1 and 8 at the bottom
    color_1_pixels = combine_pixels(object_data, [1])
    color_8_pixels = combine_pixels(object_data, [8])

    # Place combined color 1 pixels
    col_offset = 0
    for r, c in sorted(color_1_pixels, key=lambda x: x[1]): #sort by col to maintain order
      if bottom_row - (len(color_1_pixels) -1 - r) < 0: # prevent out of index error
          continue
      output_grid[bottom_row - (len(color_1_pixels) - 1 - r) , col_offset] = 1
      col_offset += 1
      if col_offset >= cols:
          col_offset = 0
    
    # Place combined color 8 pixels
    for r, c in sorted(color_8_pixels, key=lambda x: x[1]):
      if bottom_row - (len(color_8_pixels) -1 - r) < 0: # prevent out of index error
        continue
      output_grid[bottom_row - (len(color_8_pixels) -1 -r), col_offset] = 8
      col_offset += 1
      if col_offset >= cols:
          col_offset = 0
    
    # objects below row 6
    lower_objects = {k: v for k, v in object_data.items() if v['max_row'] > 6 and v['color'] not in [1, 8]}
    
    row_available = bottom_row
    if len(lower_objects) > 0:
        max_object_height = max(obj['max_row'] - obj['min_row'] + 1 for obj in lower_objects.values() )
        #row_available = bottom_row - max_object_height if bottom_row - max_object_height >= 0 else 0

        lower_pixels = combine_pixels(lower_objects, lower_objects.values())
        # sort the pixels by original row, and original column
        lower_pixels_sorted = sorted(lower_pixels, key = lambda p: (p[0], p[1]))

        row_index = bottom_row
        col_index = 0
        for r, c in lower_pixels_sorted:
            output_grid[row_index, c] = input_grid[r,c]

    # Determine row above combined objects for placing other objects
    row_above = bottom_row - 1
    if len(color_1_pixels) > 0 or len(color_8_pixels) > 0 or len(lower_objects) > 0:

        max_combined_height = 0
        if len(color_1_pixels)> 0:
          max_combined_height = max(max_combined_height, max(r for r, c in color_1_pixels) )
        if len(color_8_pixels) > 0:
          max_combined_height = max(max_combined_height, max(r for r, c in color_8_pixels) )
        
        row_above = bottom_row - (max_combined_height + 1)

    # Handle other objects
    other_objects = {k: v for k, v in object_data.items() if v['max_row'] <= 6}
    row_index = row_above
    
    for obj_id, obj_props in other_objects.items():
        # Place pixels, maintaining horizontal order
        
        for r, c in obj_props['pixels']:
            if row_index < 0:
                continue
            output_grid[row_index, c] = obj_props['color']
        row_index -= 1 #move one up

    return output_grid.tolist()