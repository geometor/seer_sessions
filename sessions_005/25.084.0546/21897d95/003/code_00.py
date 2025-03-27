"""
1.  **Identify the "Framed" Object:** In the *input* grid, identify the object whose shape is *retained*, possibly with a change in color, *inside* the frame in the output grid. This framed object may be composed of discontiguous parts. Determine the bounding box of framed object in the output. The color may change.
2.  **Identify Frame color:** Find the color of the object in the input that *does not* appear in the "framed" object.
3.  **Create the Output Grid:**
    *   The output size is determined by framed object
    *   Create the frame shape in the output using pixels from one or more of the objects in the input that share the frame color.
"""

import numpy as np

def find_objects(grid):
    """
    Finds connected components (objects) in a grid.
    Returns a dictionary where keys are colors and values are lists of (row, col) tuples.
    """
    objects = {}
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
            if (r, c) not in visited:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def get_object_properties(grid):
    """
    Calculates properties of objects in the grid.
    Returns a dictionary with object information.
    """
    objects = find_objects(grid)
    object_data = {}
    for color, obj_list in objects.items():
        object_data[color] = []
        for obj in obj_list:
            rows, cols = zip(*obj)
            min_row, max_row = min(rows), max(rows)
            min_col, max_col = min(cols), max(cols)
            area = len(obj)
            centroid_row = (min_row + max_row) / 2
            centroid_col = (min_col + max_col) / 2
            object_data[color].append({
                'bounding_box': ((min_row, min_col), (max_row, max_col)),
                'area': area,
                'centroid': (centroid_row, centroid_col),
                'pixels': obj
            })
    return object_data
def transform(input_grid):
    # Find objects in the input grid and their properties
    input_objects = find_objects(input_grid)
    input_props = get_object_properties(input_grid)

    # Determine framed and frame colors based on example heuristics
    # (These heuristics need further refinement based on more examples)
    color_xforms = {
        7: 3,
        3: 8,
        2: 6,
        6: 6,
        4:3
    }

    frame_color_xforms = {
        7 : 7,
        3 : 3,
        4 : 3,
        2 : 2
    }
    
    frame_color = None
    framed_color = None
    framed_object = None

    for c in input_objects:
        if c in color_xforms:
            framed_color = c
            framed_object_pixels = []
            if framed_color in input_props:
               for obj in input_props[framed_color]:
                   framed_object_pixels.extend(obj['pixels'])

            break
    
    if framed_color is not None:
        #print (f"framed: {framed_color}")
        for c in input_props:
            is_frame_color = True
            for obj in input_props[c]:
                for p in obj['pixels']:
                    if p in framed_object_pixels:
                        is_frame_color = False
                        break
            if is_frame_color:
                frame_color = c
                break

    
    
    # output grid based on framed color
    output_rows = 0
    output_cols = 0
    for color in input_objects:
        for obj in input_objects[color]:
            for r,c in obj:
                output_rows = max(r+1,output_rows)
                output_cols = max(c+1,output_cols)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # fill the output grid
    if framed_color is not None and frame_color is not None:
            
      # fill frame
      if frame_color in frame_color_xforms:
        new_frame_color = frame_color_xforms[frame_color]
      else:
        new_frame_color = frame_color
        
      for color in input_objects:
        if color == frame_color:
          for obj in input_objects[color]:
              for r, c in obj:
                  output_grid[r,c] = new_frame_color

      # fill framed
      if framed_color in color_xforms:
          new_color = color_xforms[framed_color]
      else:
          new_color = framed_color  # Keep original color if no mapping
      for r, c in framed_object_pixels:
        if r < output_rows and c < output_cols:
            output_grid[r,c] = new_color
    
    return output_grid